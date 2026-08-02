from django import template

register = template.Library()


@register.simple_tag
def has_socialapp(provider_id: str) -> bool:
    try:
        from allauth.socialaccount.models import SocialApp
    except Exception:
        return False

    return SocialApp.objects.filter(provider=provider_id).exists()

