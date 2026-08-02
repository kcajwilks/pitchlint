from django.urls import path

from . import views

app_name = "billing"

urlpatterns = [
    path("", views.BillingOverviewView.as_view(), name="overview"),
    path("checkout/", views.CreateCheckoutSessionView.as_view(), name="checkout"),
    path("portal/", views.CreatePortalSessionView.as_view(), name="portal"),
    path("sync/", views.AdminSyncSubscriptionView.as_view(), name="sync"),
    path("success/", views.BillingSuccessView.as_view(), name="success"),
    path("cancel/", views.BillingCancelView.as_view(), name="cancel"),
    path("webhook/", views.StripeWebhookView.as_view(), name="webhook"),
]
