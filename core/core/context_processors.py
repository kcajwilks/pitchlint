from django.conf import settings


def site(request):
    return {
        "SITE_NAME": getattr(settings, "SITE_NAME", "Acme AI"),
        "COPILOT_ENABLED": bool(getattr(settings, "COPILOT_ENABLED", False)),
    }
