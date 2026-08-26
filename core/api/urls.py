from django.urls import include, path
from rest_framework.routers import DefaultRouter

from workspace.api import ProjectViewSet

from . import auth, billing as billing_api, config

router = DefaultRouter()
router.register("projects", ProjectViewSet, basename="project")

urlpatterns = [
    path("csrf/", auth.csrf, name="api-csrf"),
    path("me/", auth.me, name="api-me"),
    path("config/", config.site_config, name="api-config"),
    path("auth/login/", auth.login_view, name="api-login"),
    path("auth/logout/", auth.logout_view, name="api-logout"),
    path("auth/signup/", auth.signup_view, name="api-signup"),
    path("billing/plans/", billing_api.plans, name="api-billing-plans"),
    path("billing/subscription/", billing_api.subscription, name="api-billing-subscription"),
    path("billing/checkout/", billing_api.checkout, name="api-billing-checkout"),
    path("billing/portal/", billing_api.portal, name="api-billing-portal"),
    path("", include(router.urls)),
]
