"""
URL configuration for core project.
"""
from pathlib import Path

from django.conf import settings
from django.contrib import admin
from django.http import FileResponse, Http404
from django.urls import include, path, re_path
from django.views.decorators.csrf import ensure_csrf_cookie

from copilot.views import runtime as copilot_runtime


def spa_index(_request):
    """Serve the Vite SPA index for client-side routes."""
    candidates = [
        Path(settings.BASE_DIR) / "static" / "spa" / "index.html",
        Path(settings.BASE_DIR) / "staticfiles" / "spa" / "index.html",
    ]
    for index in candidates:
        if index.is_file():
            return FileResponse(index.open("rb"), content_type="text/html")
    raise Http404(
        "SPA not built. Run `cd frontend && npm run build` (output: core/static/spa)."
    )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("accounts/", include("allauth.urls")),
    path("billing/webhook/", include("billing.webhook_urls")),
    path("copilot", copilot_runtime),
    path("copilot/", include("copilot.urls")),
    # SPA catch-all. Exclude API prefixes with or without a trailing slash so
    # CopilotKit's /copilot (no slash) is never served as index.html.
    re_path(
        r"^(?!api(?:/|$)|admin(?:/|$)|accounts(?:/|$)|billing/webhook(?:/|$)|copilot(?:/|$)|static(?:/|$)).*$",
        ensure_csrf_cookie(spa_index),
    ),
]
