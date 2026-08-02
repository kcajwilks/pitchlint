import os

from django.core.management.base import BaseCommand

from billing.models import Plan


class Command(BaseCommand):
    help = "Create or update default Free, Pro, and Business plans."

    def handle(self, *args, **options):
        default_plans = [
            {
                "code": "free",
                "name": "Free",
                "tagline": "Best for early product exploration.",
                "features": [
                    "Basic dashboard and settings",
                    "Email/password and Google login",
                    "Community support",
                ],
                "is_free": True,
                "highlighted": False,
                "sort_order": 0,
                "monthly_amount_cents": 0,
                "yearly_amount_cents": 0,
                "monthly_stripe_price_id": "",
                "yearly_stripe_price_id": "",
            },
            {
                "code": "pro",
                "name": "Pro",
                "tagline": "For solo builders shipping production products.",
                "features": [
                    "Everything in Free",
                    "Higher usage limits",
                    "Priority support",
                ],
                "is_free": False,
                "highlighted": True,
                "sort_order": 1,
                "monthly_amount_cents": 2900,
                "yearly_amount_cents": 29000,
                "monthly_stripe_price_id": os.getenv("STRIPE_PRICE_PRO_MONTHLY", ""),
                "yearly_stripe_price_id": os.getenv("STRIPE_PRICE_PRO_YEARLY", ""),
            },
            {
                "code": "business",
                "name": "Business",
                "tagline": "For teams scaling AI products across use cases.",
                "features": [
                    "Everything in Pro",
                    "Team-ready workflows",
                    "Premium support",
                ],
                "is_free": False,
                "highlighted": False,
                "sort_order": 2,
                "monthly_amount_cents": 9900,
                "yearly_amount_cents": 99000,
                "monthly_stripe_price_id": os.getenv("STRIPE_PRICE_BUSINESS_MONTHLY", ""),
                "yearly_stripe_price_id": os.getenv("STRIPE_PRICE_BUSINESS_YEARLY", ""),
            },
        ]

        for attrs in default_plans:
            code = attrs["code"]
            Plan.objects.update_or_create(code=code, defaults=attrs)
            self.stdout.write(self.style.SUCCESS(f"Seeded plan: {code}"))
