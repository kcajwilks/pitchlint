import stripe
from django.conf import settings
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from billing.models import Plan
from billing.services import (
    create_checkout_session,
    create_portal_session,
    get_or_create_local_subscription,
)


def _missing_stripe_settings() -> list[str]:
    required = {
        "STRIPE_SECRET_KEY": getattr(settings, "STRIPE_SECRET_KEY", "") or "",
        "STRIPE_PUBLIC_KEY": getattr(settings, "STRIPE_PUBLIC_KEY", "") or "",
        "STRIPE_WEBHOOK_SECRET": getattr(settings, "STRIPE_WEBHOOK_SECRET", "") or "",
    }
    return [key for key, value in required.items() if not str(value).strip()]


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def plans(request):
    qs = Plan.objects.filter(active=True).order_by("sort_order", "name")
    data = [
        {
            "code": p.code,
            "name": p.name,
            "tagline": p.tagline,
            "features": p.features,
            "is_free": p.is_free,
            "highlighted": p.highlighted,
            "monthly_amount_cents": p.monthly_amount_cents,
            "yearly_amount_cents": p.yearly_amount_cents,
        }
        for p in qs
    ]
    return Response(
        {
            "plans": data,
            "billing_enabled": not _missing_stripe_settings(),
            "missing_env": _missing_stripe_settings(),
            "stripe_public_key": getattr(settings, "STRIPE_PUBLIC_KEY", "") or "",
        }
    )


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def subscription(request):
    sub = get_or_create_local_subscription(request.user)
    return Response(
        {
            "status": sub.status,
            "plan_code": sub.plan.code if sub.plan_id else None,
            "plan_name": sub.plan.name if sub.plan_id else None,
            "current_period_end": sub.current_period_end.isoformat() if sub.current_period_end else None,
        }
    )


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def checkout(request):
    if _missing_stripe_settings():
        return Response(
            {"detail": "Billing is not configured.", "missing_env": _missing_stripe_settings()},
            status=status.HTTP_400_BAD_REQUEST,
        )

    plan_code = (request.data.get("plan_code") or "").strip()
    interval = (request.data.get("interval") or "monthly").strip().lower()
    plan = Plan.objects.filter(code=plan_code, active=True).first()
    if not plan:
        return Response({"detail": "Invalid plan."}, status=status.HTTP_400_BAD_REQUEST)
    if plan.is_free:
        return Response({"detail": "Free plan does not require checkout."}, status=status.HTTP_400_BAD_REQUEST)
    if interval not in {"monthly", "yearly"}:
        return Response({"detail": "Invalid interval."}, status=status.HTTP_400_BAD_REQUEST)

    origin = request.headers.get("Origin") or request.build_absolute_uri("/").rstrip("/")
    success_url = f"{origin}/settings/billing?checkout=success"
    cancel_url = f"{origin}/settings/billing?checkout=cancel"
    try:
        session = create_checkout_session(
            user=request.user,
            plan=plan,
            success_url=success_url,
            cancel_url=cancel_url,
            interval=interval,
        )
    except stripe.error.StripeError as exc:
        return Response({"detail": exc.user_message or str(exc)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response({"detail": "Unable to start checkout."}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"url": session.url})


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def portal(request):
    if _missing_stripe_settings():
        return Response({"detail": "Billing is not configured."}, status=status.HTTP_400_BAD_REQUEST)
    origin = request.headers.get("Origin") or request.build_absolute_uri("/").rstrip("/")
    return_url = f"{origin}/settings/billing"
    try:
        session = create_portal_session(user=request.user, return_url=return_url)
    except Exception:
        return Response({"detail": "Unable to open billing portal."}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"url": session.url})
