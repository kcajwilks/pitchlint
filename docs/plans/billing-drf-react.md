---
status: Pending Review
owner: Jack Wilkins
created: 2026-08-26
updated: 2026-08-26
---

# Billing + settings via API and React

## Context

Full cutover includes pricing, billing settings, Stripe checkout/portal from the SPA.

## Findings

- `core/billing/` services (checkout, portal, webhook) already exist.
- Templates: `billing/`, `settings/billing.html`, `pricing.html`.

## Root Cause

Billing UX is HTML; SPA needs JSON plan catalog + checkout session creation.

## Proposed Solution

DRF endpoints for plans, subscription status, create checkout/portal session (reuse services); React pricing + settings billing pages; webhook stays Django view.

**Starter mapping**
- reuse: `billing/services.py`, webhook, `seed_plans`, permissions
- extend: billing with API views
- new: React pricing/settings billing

## Implementation Steps

- [ ] API: list plans, subscription summary, checkout, portal
- [ ] React: pricing, settings billing
- [ ] Keep webhook at `/billing/webhook/` (not SPA)
- [ ] Gate sample features with existing subscription helpers where appropriate

## Risks & Dependencies

- Stripe redirect return URLs must point at SPA routes
- Depends on: spa-drf-foundation, spa-auth-allauth, spa-app-shell

## Expected Outcome

User can view plans and start Stripe checkout/portal from React; webhooks still sync subscriptions.

---
Owner: Jack Wilkins
Last reviewed: 2026-08-26
Review cadence: on change
