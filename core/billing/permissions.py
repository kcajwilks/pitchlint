from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

from .services import has_active_subscription


def subscription_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if has_active_subscription(request.user):
            return view_func(request, *args, **kwargs)
        messages.warning(request, "An active subscription is required for this feature.")
        return redirect("billing:overview")

    return _wrapped


class SubscriptionRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if has_active_subscription(request.user):
            return super().dispatch(request, *args, **kwargs)
        messages.warning(request, "An active subscription is required for this feature.")
        return redirect("billing:overview")
