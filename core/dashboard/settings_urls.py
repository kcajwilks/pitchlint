from django.urls import path

from . import views

app_name = "settings"

urlpatterns = [
    path("profile/", views.ProfileSettingsView.as_view(), name="profile"),
    path("account/", views.AccountSettingsView.as_view(), name="account"),
    path("billing/", views.BillingSettingsView.as_view(), name="billing"),
    path("account/delete/", views.DeleteAccountView.as_view(), name="delete_account"),
]
