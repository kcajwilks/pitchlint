from django.contrib.auth import authenticate, get_user_model, login, logout
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

User = get_user_model()


def _user_payload(user):
    return {
        "id": user.pk,
        "email": getattr(user, "email", "") or user.get_username(),
        "username": user.get_username(),
        "is_staff": user.is_staff,
    }


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
@ensure_csrf_cookie
def csrf(request):
    return Response({"csrfToken": get_token(request)})


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def me(request):
    if not request.user.is_authenticated:
        return Response({"authenticated": False, "user": None})
    return Response({"authenticated": True, "user": _user_payload(request.user)})


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def login_view(request):
    email = (request.data.get("email") or "").strip()
    password = request.data.get("password") or ""
    if not email or not password:
        return Response({"detail": "Email and password required."}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=email, password=password)
    if user is None:
        # allauth email-as-username: try lookup by email
        try:
            account = User.objects.get(email__iexact=email)
            user = authenticate(request, username=account.get_username(), password=password)
        except User.DoesNotExist:
            user = None

    if user is None:
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

    login(request, user)
    return Response({"authenticated": True, "user": _user_payload(user)})


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({"ok": True})


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def signup_view(request):
    email = (request.data.get("email") or "").strip().lower()
    password = request.data.get("password") or ""
    if not email or not password:
        return Response({"detail": "Email and password required."}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(email__iexact=email).exists():
        return Response({"detail": "An account with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=email, email=email, password=password)
    login(request, user, backend="django.contrib.auth.backends.ModelBackend")
    return Response({"authenticated": True, "user": _user_payload(user)}, status=status.HTTP_201_CREATED)
