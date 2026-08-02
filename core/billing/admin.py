from django.contrib import admin

from .models import BillingEvent, Plan, Subscription


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "is_free", "highlighted", "active", "sort_order")
    list_filter = ("active", "is_free", "highlighted")
    search_fields = ("name", "code", "monthly_stripe_price_id", "yearly_stripe_price_id")
    ordering = ("sort_order", "name")


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "plan",
        "status",
        "cancel_at_period_end",
        "current_period_end",
        "updated_at",
    )
    list_filter = ("status", "cancel_at_period_end", "plan")
    search_fields = ("user__email", "stripe_customer_id", "stripe_subscription_id")
    autocomplete_fields = ("user", "plan")
    readonly_fields = ("raw_payload", "created_at", "updated_at")


@admin.register(BillingEvent)
class BillingEventAdmin(admin.ModelAdmin):
    list_display = ("stripe_event_id", "event_type", "processed_at")
    search_fields = ("stripe_event_id", "event_type")
    readonly_fields = ("payload", "processed_at")
