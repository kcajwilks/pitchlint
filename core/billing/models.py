from django.conf import settings
from django.db import models


class Plan(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=120)
    tagline = models.CharField(max_length=200, blank=True)
    features = models.JSONField(default=list, blank=True)
    monthly_stripe_price_id = models.CharField(max_length=120, blank=True)
    yearly_stripe_price_id = models.CharField(max_length=120, blank=True)
    monthly_amount_cents = models.PositiveIntegerField(null=True, blank=True)
    yearly_amount_cents = models.PositiveIntegerField(null=True, blank=True)
    is_free = models.BooleanField(default=False)
    highlighted = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name


class Subscription(models.Model):
    STATUS_INCOMPLETE = "incomplete"
    STATUS_INCOMPLETE_EXPIRED = "incomplete_expired"
    STATUS_TRIALING = "trialing"
    STATUS_ACTIVE = "active"
    STATUS_PAST_DUE = "past_due"
    STATUS_CANCELED = "canceled"
    STATUS_UNPAID = "unpaid"
    STATUS_PAUSED = "paused"

    STATUS_CHOICES = [
        (STATUS_INCOMPLETE, "Incomplete"),
        (STATUS_INCOMPLETE_EXPIRED, "Incomplete Expired"),
        (STATUS_TRIALING, "Trialing"),
        (STATUS_ACTIVE, "Active"),
        (STATUS_PAST_DUE, "Past Due"),
        (STATUS_CANCELED, "Canceled"),
        (STATUS_UNPAID, "Unpaid"),
        (STATUS_PAUSED, "Paused"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscription",
    )
    plan = models.ForeignKey(
        Plan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subscriptions",
    )
    stripe_customer_id = models.CharField(max_length=120, blank=True)
    stripe_subscription_id = models.CharField(max_length=120, blank=True)
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default=STATUS_INCOMPLETE,
    )
    current_period_start = models.DateTimeField(null=True, blank=True)
    current_period_end = models.DateTimeField(null=True, blank=True)
    cancel_at_period_end = models.BooleanField(default=False)
    raw_payload = models.JSONField(default=dict, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.user} ({self.status})"


class BillingEvent(models.Model):
    stripe_event_id = models.CharField(max_length=120, unique=True)
    event_type = models.CharField(max_length=120)
    payload = models.JSONField(default=dict, blank=True)
    processed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-processed_at"]

    def __str__(self):
        return self.stripe_event_id
