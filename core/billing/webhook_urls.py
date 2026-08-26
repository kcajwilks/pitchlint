from django.urls import path

from billing.views import StripeWebhookView

urlpatterns = [
    path("", StripeWebhookView.as_view(), name="webhook"),
]
