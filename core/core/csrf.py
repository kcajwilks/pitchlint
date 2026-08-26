from django.http import JsonResponse
from django.views.csrf import csrf_failure as django_csrf_failure


def csrf_failure(request, reason=""):
    if request.path.startswith("/api/") or request.path.startswith("/copilot"):
        return JsonResponse(
            {"error": "CSRF verification failed.", "detail": str(reason)},
            status=403,
        )
    return django_csrf_failure(request, reason=reason)
