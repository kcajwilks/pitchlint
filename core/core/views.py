"""
Views for core.
"""
from django.views.generic import TemplateView

from billing.models import Plan


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["plans"] = Plan.objects.filter(active=True).order_by("sort_order", "name")
        return context


class PricingView(TemplateView):
    template_name = "pricing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["plans"] = Plan.objects.filter(active=True).order_by("sort_order", "name")
        return context
