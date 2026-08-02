from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView

from billing.models import Plan
from billing.services import get_or_create_local_subscription


def _billing_enabled() -> bool:
    required = [
        getattr(settings, "STRIPE_SECRET_KEY", ""),
        getattr(settings, "STRIPE_PUBLIC_KEY", ""),
        getattr(settings, "STRIPE_WEBHOOK_SECRET", ""),
    ]
    return all(str(value).strip() for value in required)


class DashboardHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    login_url = 'account_login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subscription = getattr(self.request.user, "subscription", None)
        context["subscription"] = subscription
        context["is_free"] = not (subscription and subscription.plan)
        context["usage_metrics"] = [
            {"label": "Agent runs", "value": 0, "hint": "Hook your product metrics here"},
            {"label": "Requests", "value": 0, "hint": "Track monthly request count"},
            {"label": "Active automations", "value": 0, "hint": "Map to your workflows"},
            {"label": "Team seats", "value": 1, "hint": "Single-user starter by default"},
        ]
        context["active_nav"] = "dashboard"
        context["app_page_title"] = "Dashboard"
        return context


class ProfileSettingsView(LoginRequiredMixin, TemplateView):
    template_name = "settings/profile.html"
    login_url = "account_login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "settings"
        context["settings_tab"] = "profile"
        context["app_page_title"] = "Settings"
        return context


class AccountSettingsView(LoginRequiredMixin, TemplateView):
    template_name = "settings/account.html"
    login_url = "account_login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "settings"
        context["settings_tab"] = "account"
        context["app_page_title"] = "Settings"
        return context


class BillingSettingsView(LoginRequiredMixin, TemplateView):
    template_name = "settings/billing.html"
    login_url = "account_login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "settings"
        context["settings_tab"] = "billing"
        context["billing_enabled"] = _billing_enabled()
        context["plans"] = Plan.objects.filter(active=True).order_by("sort_order", "name")
        context["subscription"] = get_or_create_local_subscription(self.request.user)
        context["app_page_title"] = "Settings"
        return context


class DeleteAccountView(LoginRequiredMixin, View):
    login_url = 'account_login'

    def get(self, request):
        return render(request, 'settings/delete_account.html')

    def post(self, request):
        if request.POST.get('confirm_delete') != 'yes':
            return render(
                request,
                'settings/delete_account.html',
                {'error': 'Please confirm account deletion to continue.'},
            )
        user = request.user
        logout(request)
        user.delete()
        return redirect('home')
