from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import override_settings
from django.test import TestCase
from django.urls import reverse

from .models import BillingEvent, Plan, Subscription
from .services import (
    create_checkout_session,
    get_or_create_stripe_customer,
    handle_webhook_event,
    has_active_subscription,
)

User = get_user_model()


class BillingServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="billing-user",
            email="billing@example.com",
            password="password123",
        )
        self.plan = Plan.objects.create(
            code="pro",
            name="Pro",
            monthly_stripe_price_id="price_pro_monthly",
            yearly_stripe_price_id="price_pro_yearly",
            monthly_amount_cents=2900,
            yearly_amount_cents=29000,
            active=True,
            sort_order=1,
        )

    @patch("billing.services.stripe.Customer.create")
    def test_get_or_create_stripe_customer_creates_and_reuses_customer(self, mock_create):
        mock_create.return_value = {"id": "cus_123"}

        customer_id = get_or_create_stripe_customer(self.user)
        self.assertEqual(customer_id, "cus_123")
        self.assertEqual(mock_create.call_count, 1)

        customer_id_again = get_or_create_stripe_customer(self.user)
        self.assertEqual(customer_id_again, "cus_123")
        self.assertEqual(mock_create.call_count, 1)

    @patch("billing.services.stripe.checkout.Session.create")
    @patch("billing.services.get_or_create_stripe_customer")
    def test_create_checkout_session_for_plan(
        self, mock_get_customer, mock_checkout_create
    ):
        mock_get_customer.return_value = "cus_123"
        mock_checkout_create.return_value = {"id": "cs_test", "url": "https://checkout"}

        session = create_checkout_session(
            user=self.user,
            plan=self.plan,
            success_url="https://example.com/success",
            cancel_url="https://example.com/cancel",
            interval="yearly",
        )

        self.assertEqual(session["id"], "cs_test")
        kwargs = mock_checkout_create.call_args.kwargs
        self.assertEqual(kwargs["line_items"][0]["price"], self.plan.yearly_stripe_price_id)
        self.assertEqual(kwargs["customer"], "cus_123")

    def test_has_active_subscription_only_for_active_or_trialing(self):
        subscription = Subscription.objects.create(
            user=self.user,
            status=Subscription.STATUS_CANCELED,
        )
        self.assertFalse(has_active_subscription(self.user))

        subscription.status = Subscription.STATUS_ACTIVE
        subscription.save(update_fields=["status", "updated_at"])
        self.assertTrue(has_active_subscription(self.user))

        subscription.status = Subscription.STATUS_TRIALING
        subscription.save(update_fields=["status", "updated_at"])
        self.assertTrue(has_active_subscription(self.user))

        subscription.status = Subscription.STATUS_PAST_DUE
        subscription.save(update_fields=["status", "updated_at"])
        self.assertFalse(has_active_subscription(self.user))


class BillingWebhookTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="webhook-user",
            email="webhook@example.com",
            password="password123",
        )
        self.plan = Plan.objects.create(
            code="team",
            name="Team",
            monthly_stripe_price_id="price_team_monthly",
            yearly_stripe_price_id="price_team_yearly",
            active=True,
            sort_order=2,
        )
        self.subscription = Subscription.objects.create(
            user=self.user,
            stripe_customer_id="cus_webhook_1",
        )

    def _subscription_event(self, event_id, status):
        return {
            "id": event_id,
            "type": "customer.subscription.updated",
            "data": {
                "object": {
                    "id": "sub_123",
                    "customer": "cus_webhook_1",
                    "status": status,
                    "current_period_start": 1710000000,
                    "current_period_end": 1712592000,
                    "cancel_at_period_end": False,
                    "items": {"data": [{"price": {"id": "price_team_monthly"}}]},
                }
            },
        }

    def test_webhook_idempotency(self):
        event = self._subscription_event("evt_1", "active")
        handle_webhook_event(event)
        handle_webhook_event(event)

        self.assertEqual(BillingEvent.objects.filter(stripe_event_id="evt_1").count(), 1)

    def test_webhook_lifecycle_transition_updates_local_subscription(self):
        for event_id, status in [
            ("evt_active", "active"),
            ("evt_past_due", "past_due"),
            ("evt_canceled", "canceled"),
        ]:
            handle_webhook_event(self._subscription_event(event_id, status))
            self.subscription.refresh_from_db()
            self.assertEqual(self.subscription.status, status)
            self.assertEqual(self.subscription.plan, self.plan)


class BillingViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="view-user",
            email="view@example.com",
            password="password123",
        )
        self.plan = Plan.objects.create(
            code="starter",
            name="Starter",
            monthly_stripe_price_id="price_starter_monthly",
            yearly_stripe_price_id="price_starter_yearly",
            active=True,
            sort_order=0,
        )
        self.client.login(username="view-user", password="password123")

    @override_settings(
        STRIPE_SECRET_KEY="",
        STRIPE_PUBLIC_KEY="",
        STRIPE_WEBHOOK_SECRET="",
    )
    def test_billing_overview_context_disables_billing_when_missing_stripe_settings(self):
        response = self.client.get(reverse("billing:overview"))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["billing_enabled"])
        self.assertEqual(
            set(response.context["missing_stripe_env_vars"]),
            {"STRIPE_SECRET_KEY", "STRIPE_PUBLIC_KEY", "STRIPE_WEBHOOK_SECRET"},
        )

    @patch("billing.views.create_checkout_session")
    @override_settings(
        STRIPE_SECRET_KEY="sk_test_x",
        STRIPE_PUBLIC_KEY="pk_test_x",
        STRIPE_WEBHOOK_SECRET="whsec_x",
    )
    def test_checkout_view_redirects_to_stripe_checkout_url(self, mock_create_checkout):
        mock_create_checkout.return_value = SimpleNamespace(url="https://checkout.example")

        response = self.client.post(
            reverse("billing:checkout"),
            data={"plan_code": self.plan.code, "interval": "yearly"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "https://checkout.example")
        self.assertEqual(mock_create_checkout.call_args.kwargs["interval"], "yearly")

    def test_webhook_view_rejects_missing_signature_header(self):
        response = self.client.post(
            reverse("billing:webhook"),
            data=b"{}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)


class BillingAdminSyncTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="sync-user",
            email="sync@example.com",
            password="password123",
        )
        self.staff = User.objects.create_user(
            username="staff-user",
            email="staff@example.com",
            password="password123",
            is_staff=True,
        )

    def test_sync_endpoint_forbidden_for_non_staff(self):
        self.client.login(username="sync-user", password="password123")
        response = self.client.post(reverse("billing:sync"))
        self.assertEqual(response.status_code, 403)

    @patch("billing.views.sync_subscription_from_stripe")
    @patch("billing.views.stripe.Subscription.list")
    @override_settings(
        STRIPE_SECRET_KEY="sk_test_x",
        STRIPE_PUBLIC_KEY="pk_test_x",
        STRIPE_WEBHOOK_SECRET="whsec_x",
    )
    def test_sync_endpoint_lists_customer_subscriptions_and_syncs(
        self, mock_list, mock_sync
    ):
        Subscription.objects.create(user=self.staff, stripe_customer_id="cus_123")
        mock_list.return_value = {
            "data": [
                {
                    "id": "sub_1",
                    "customer": "cus_123",
                    "status": "active",
                    "current_period_start": 1710000000,
                    "current_period_end": 1712592000,
                    "cancel_at_period_end": False,
                    "items": {"data": [{"price": {"id": "price_starter_monthly"}}]},
                    "created": 1710000001,
                }
            ]
        }
        mock_sync.return_value = Subscription.objects.get(user=self.staff)

        self.client.login(username="staff-user", password="password123")
        response = self.client.post(reverse("billing:sync"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("settings:billing"))
        self.assertEqual(mock_list.call_count, 1)
        self.assertEqual(mock_sync.call_count, 1)
