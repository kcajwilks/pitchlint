from django.conf import settings
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def site_config(request):
    return Response(
        {
            "site_name": getattr(settings, "SITE_NAME", "SaaS Starter"),
            "copilot_enabled": bool(getattr(settings, "COPILOT_ENABLED", False)),
        }
    )
