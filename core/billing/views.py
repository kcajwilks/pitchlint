import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from .models import Plan
from .services import (
    create_checkout_session,
    create_portal_session,
    get_or_create_local_subscription,
    handle_webhook_event,
    sync_subscription_from_stripe,
    verify_webhook_event,
)


def _missing_stripe_settings() -> list[str]:
    required = {
        "STRIPE_SECRET_KEY": getattr(settings, "STRIPE_SECRET_KEY", "") or "",
        "STRIPE_PUBLIC_KEY": getattr(settings, "STRIPE_PUBLIC_KEY", "") or "",
        "STRIPE_WEBHOOK_SECRET": getattr(settings, "STRIPE_WEBHOOK_SECRET", "") or "",
    }
    return [key for key, value in required.items() if not str(value).strip()]


def _billing_enabled() -> bool:
    return not _missing_stripe_settings()


class BillingOverviewView(LoginRequiredMixin, TemplateView):
    template_name = "billing/overview.html"
    login_url = "account_login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        missing = _missing_stripe_settings()
        context["billing_enabled"] = not missing
        context["missing_stripe_env_vars"] = missing
        context["plans"] = Plan.objects.filter(active=True).order_by("sort_order", "name")
        context["subscription"] = get_or_create_local_subscription(self.request.user)
        context["active_nav"] = "settings"
        context["app_page_title"] = "Billing"
        return context


class BillingSuccessView(LoginRequiredMixin, View):
    login_url = "account_login"

    def get(self, request, *args, **kwargs):
        messages.success(
            request,
            "Checkout completed. Your subscription will appear after the Stripe webhook syncs.",
        )
        return redirect("settings:billing")


class BillingCancelView(LoginRequiredMixin, View):
    login_url = "account_login"

    def get(self, request, *args, **kwargs):
        messages.info(request, "Checkout canceled.")
        return redirect("settings:billing")


class CreateCheckoutSessionView(LoginRequiredMixin, View):
    login_url = "account_login"

    def post(self, request, *args, **kwargs):
        if not _billing_enabled():
            messages.error(
                request,
                "Billing is not configured. Set STRIPE_SECRET_KEY, STRIPE_PUBLIC_KEY, and STRIPE_WEBHOOK_SECRET.",
            )
            return redirect("settings:billing")

        plan_code = request.POST.get("plan_code", "").strip()
        plan = Plan.objects.filter(code=plan_code, active=True).first()
        if not plan:
            messages.error(request, "Invalid plan selected.")
            return redirect("settings:billing")
        if plan.is_free:
            messages.info(request, "You are already on the free tier.")
            return redirect("settings:billing")

        interval = request.POST.get("interval", "monthly").strip().lower()
        if interval not in {"monthly", "yearly"}:
            messages.error(request, "Invalid billing interval selected.")
            return redirect("settings:billing")

        success_url = request.build_absolute_uri(reverse("billing:success"))
        cancel_url = request.build_absolute_uri(reverse("billing:cancel"))
        try:
            session = create_checkout_session(
                user=request.user,
                plan=plan,
                success_url=success_url,
                cancel_url=cancel_url,
                interval=interval,
            )
        except stripe.error.StripeError as exc:
            messages.error(request, f"Stripe error: {exc.user_message or str(exc)}")
            return redirect("settings:billing")
        except Exception:
            messages.error(request, "Unable to start checkout session.")
            return redirect("settings:billing")
        return redirect(session.url)


class CreatePortalSessionView(LoginRequiredMixin, View):
    login_url = "account_login"

    def post(self, request, *args, **kwargs):
        if not _billing_enabled():
            messages.error(
                request,
                "Billing portal is not available until Stripe is configured.",
            )
            return redirect("settings:billing")

        return_url = request.build_absolute_uri(reverse("settings:billing"))
        try:
            session = create_portal_session(user=request.user, return_url=return_url)
        except stripe.error.StripeError as exc:
            messages.error(request, f"Stripe error: {exc.user_message or str(exc)}")
            return redirect("settings:billing")
        except Exception:
            messages.error(request, "Unable to open billing portal.")
            return redirect("settings:billing")
        return redirect(session.url)


class AdminSyncSubscriptionView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = "account_login"
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return bool(user and user.is_authenticated and (user.is_staff or user.is_superuser))

    def post(self, request, *args, **kwargs):
        if not _billing_enabled():
            messages.error(
                request,
                "Billing is not configured. Set STRIPE_SECRET_KEY, STRIPE_PUBLIC_KEY, and STRIPE_WEBHOOK_SECRET.",
            )
            return redirect("settings:billing")

        subscription = get_or_create_local_subscription(request.user)
        try:
            from .services import configure_stripe

            configure_stripe()

            stripe_subscription = None
            if subscription.stripe_subscription_id:
                stripe_subscription = stripe.Subscription.retrieve(
                    subscription.stripe_subscription_id
                )
            elif subscription.stripe_customer_id:
                result = stripe.Subscription.list(
                    customer=subscription.stripe_customer_id,
                    status="all",
                    limit=10,
                )
                data = result.get("data", []) if isinstance(result, dict) else []
                if data:
                    preferred = next(
                        (s for s in data if s.get("status") in {"active", "trialing"}),
                        None,
                    )
                    stripe_subscription = preferred or sorted(
                        data, key=lambda s: s.get("created", 0), reverse=True
                    )[0]

            if not stripe_subscription:
                messages.warning(request, "No Stripe subscription found to sync.")
                return redirect("settings:billing")

            synced = sync_subscription_from_stripe(
                stripe_subscription, fallback_user_id=request.user.id
            )
            if not synced:
                messages.warning(request, "Unable to sync subscription from Stripe.")
            else:
                messages.success(request, "Subscription synced from Stripe.")
        except stripe.error.StripeError as exc:
            messages.error(request, f"Stripe error: {exc.user_message or str(exc)}")
        except Exception:
            messages.error(request, "Unable to sync subscription from Stripe.")

        return redirect("settings:billing")



@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(View):
    def post(self, request, *args, **kwargs):
        signature = request.META.get("HTTP_STRIPE_SIGNATURE", "")
        if not signature:
            return HttpResponseBadRequest("Missing Stripe signature.")

        try:
            event = verify_webhook_event(request.body, signature)
        except ValueError as exc:
            return HttpResponseBadRequest(str(exc))
        except stripe.error.SignatureVerificationError:
            return HttpResponseBadRequest("Invalid Stripe signature.")
        except Exception:
            return HttpResponseBadRequest("Webhook verification failed.")

        handle_webhook_event(event)
        return JsonResponse({"received": True})
