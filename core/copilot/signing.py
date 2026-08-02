import json

from django.conf import settings
from django.core import signing


def sign_action(payload: dict, *, max_age_seconds: int = 15 * 60) -> str:
    signer = signing.TimestampSigner(salt="copilot.action")
    value = json.dumps(payload, separators=(",", ":"), sort_keys=True)
    signed = signer.sign(value)
    # max_age_seconds is enforced when verifying; included here for readability/documentation.
    _ = max_age_seconds
    return signed


def unsign_action(token: str, *, max_age_seconds: int = 15 * 60) -> dict:
    signer = signing.TimestampSigner(salt="copilot.action")
    value = signer.unsign(token, max_age=max_age_seconds)
    return json.loads(value)

