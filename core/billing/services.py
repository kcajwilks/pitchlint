from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

import stripe
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from .models import BillingEvent, Plan, Subscription

User = get_user_model()


SUBSCRIPTION_ACTIVE_STATUSES = {
    Subscription.STATUS_ACTIVE,
    Subscription.STATUS_TRIALING,
}


def configure_stripe() -> None:
    stripe.api_key = settings.STRIPE_SECRET_KEY


def has_active_subscription(user) -> bool:
    if not user.is_authenticated:
        return False
    try:
        subscription = user.subscription
    except Subscription.DoesNotExist:
        return False
    return subscription.status in SUBSCRIPTION_ACTIVE_STATUSES


def get_or_create_local_subscription(user) -> Subscription:
    subscription, _ = Subscription.objects.get_or_create(user=user)
    return subscription


def get_or_create_stripe_customer(user) -> str:
    configure_stripe()
    subscription = get_or_create_local_subscription(user)
    if subscription.stripe_customer_id:
        return subscription.stripe_customer_id

    customer = stripe.Customer.create(
        email=user.email,
        metadata={"user_id": str(user.id)},
    )
    subscription.stripe_customer_id = customer["id"]
    subscription.save(update_fields=["stripe_customer_id", "updated_at"])
    return subscription.stripe_customer_id


def create_checkout_session(
    user,
    plan: Plan,
    success_url: str,
    cancel_url: str,
    interval: str = "monthly",
):
    configure_stripe()
    customer_id = get_or_create_stripe_customer(user)
    price_id = (
        plan.yearly_stripe_price_id
        if interval == "yearly"
        else plan.monthly_stripe_price_id
    )
    if not price_id:
        raise ValueError("Selected plan is missing Stripe price configuration.")

    session = stripe.checkout.Session.create(
        customer=customer_id,
        mode="subscription",
        payment_method_types=["card"],
        line_items=[{"price": price_id, "quantity": 1}],
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={"user_id": str(user.id), "plan_code": plan.code, "interval": interval},
    )
    return session


def create_portal_session(user, return_url: str):
    configure_stripe()
    customer_id = get_or_create_stripe_customer(user)
    return stripe.billing_portal.Session.create(
        customer=customer_id,
        return_url=return_url,
    )


def verify_webhook_event(payload: bytes, signature_header: str):
    configure_stripe()
    if not settings.STRIPE_WEBHOOK_SECRET:
        raise ValueError("STRIPE_WEBHOOK_SECRET is not configured.")
    return stripe.Webhook.construct_event(
        payload=payload,
        sig_header=signature_header,
        secret=settings.STRIPE_WEBHOOK_SECRET,
    )


def _from_unix_timestamp(value: Optional[int]):
    if not value:
        return None
    return datetime.fromtimestamp(value, tz=timezone.utc)


def _extract_price_id(stripe_subscription: dict[str, Any]) -> str:
    items = stripe_subscription.get("items", {}).get("data", [])
    if not items:
        return ""
    price = items[0].get("price", {})
    return price.get("id", "")


def _resolve_user_id_for_subscription(
    stripe_subscription: dict[str, Any], fallback_user_id: Optional[int] = None
) -> Optional[int]:
    customer_id = stripe_subscription.get("customer")
    if customer_id:
        existing = Subscription.objects.filter(stripe_customer_id=customer_id).first()
        if existing:
            return existing.user_id
    if fallback_user_id:
        return fallback_user_id
    return None


@transaction.atomic
def sync_subscription_from_stripe(
    stripe_subscription: dict[str, Any], fallback_user_id: Optional[int] = None
) -> Optional[Subscription]:
    user_id = _resolve_user_id_for_subscription(stripe_subscription, fallback_user_id)
    if not user_id:
        return None

    user = User.objects.filter(id=user_id).first()
    if not user:
        return None

    subscription = get_or_create_local_subscription(user)
    customer_id = stripe_subscription.get("customer", "")
    if customer_id:
        subscription.stripe_customer_id = customer_id
    subscription.stripe_subscription_id = stripe_subscription.get("id", "")
    subscription.status = stripe_subscription.get("status", Subscription.STATUS_INCOMPLETE)
    subscription.current_period_start = _from_unix_timestamp(
        stripe_subscription.get("current_period_start")
    )
    subscription.current_period_end = _from_unix_timestamp(
        stripe_subscription.get("current_period_end")
    )
    subscription.cancel_at_period_end = bool(
        stripe_subscription.get("cancel_at_period_end", False)
    )
    subscription.raw_payload = stripe_subscription

    price_id = _extract_price_id(stripe_subscription)
    subscription.plan = Plan.objects.filter(active=True).filter(
        Q(monthly_stripe_price_id=price_id) | Q(yearly_stripe_price_id=price_id)
    ).first()
    subscription.save()
    return subscription


def _track_event(event: dict[str, Any]) -> bool:
    _, created = BillingEvent.objects.get_or_create(
        stripe_event_id=event["id"],
        defaults={
            "event_type": event["type"],
            "payload": event,
        },
    )
    return created


def handle_webhook_event(event: dict[str, Any]) -> Optional[Subscription]:
    if not _track_event(event):
        return None

    event_type = event.get("type")
    event_data = event.get("data", {}).get("object", {})

    if event_type == "checkout.session.completed":
        user_id = event_data.get("metadata", {}).get("user_id")
        customer_id = event_data.get("customer")
        if user_id and customer_id:
            subscription = Subscription.objects.filter(user_id=user_id).first()
            if not subscription:
                user = User.objects.filter(id=user_id).first()
                if user:
                    subscription = get_or_create_local_subscription(user)
            if subscription:
                subscription.stripe_customer_id = customer_id
                subscription.save(update_fields=["stripe_customer_id", "updated_at"])
        return None

    if event_type in {
        "customer.subscription.created",
        "customer.subscription.updated",
        "customer.subscription.deleted",
    }:
        return sync_subscription_from_stripe(event_data)

    return None
