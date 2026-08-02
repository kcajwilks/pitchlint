# Stripe setup (products, prices, webhooks)

This starter integrates Stripe Checkout, Billing Portal, and a webhook endpoint at:

- `POST /billing/webhook/`

It stores billing state in the local `billing.Subscription` model and syncs it from Stripe webhooks.

## 1) Create products + prices in Stripe

In your Stripe Dashboard:

- Create a **Product** for each paid plan (for example: Pro, Business)
- Create **recurring Prices** for each product:
  - Monthly price
  - Yearly price

Copy the Stripe **Price IDs** (they look like `price_...`).

## 2) Put price IDs into environment variables (for seeding)

The `seed_plans` command can attach Stripe prices to the default plans using these env vars:

- `STRIPE_PRICE_PRO_MONTHLY`
- `STRIPE_PRICE_PRO_YEARLY`
- `STRIPE_PRICE_BUSINESS_MONTHLY`
- `STRIPE_PRICE_BUSINESS_YEARLY`

Add them to `core/.env` (local), or to your platform’s environment variables (prod).

Then run:

```bash
cd core
python manage.py seed_plans
```

## 3) Configure Stripe API keys

Set these in `core/.env`:

- `STRIPE_SECRET_KEY` (starts with `sk_...`)
- `STRIPE_PUBLIC_KEY` (starts with `pk_...`)

## 4) Configure the Stripe Billing Portal

In Stripe Dashboard:

- Enable/configure the **Customer Portal**
- Set which features customers can manage (cancel, update payment method, invoices, etc.)

This starter uses the portal session API and sends users back to `/settings/billing/`.

## 5) Configure webhooks (local development)

Install the Stripe CLI and authenticate, then forward events to your local server:

```bash
stripe listen --forward-to http://127.0.0.1:8000/billing/webhook/
```

The CLI will print a webhook signing secret like `whsec_...`.
Copy it into `core/.env` as:

- `STRIPE_WEBHOOK_SECRET`

### Events

This starter syncs subscriptions from these events:

- `customer.subscription.created`
- `customer.subscription.updated`
- `customer.subscription.deleted`

It also records the customer ID on:

- `checkout.session.completed`

## 6) Configure webhooks (production)

In Stripe Dashboard, add a webhook endpoint:

- URL: `https://YOUR_DOMAIN/billing/webhook/`
- Events: at minimum the subscription events above

Set `STRIPE_WEBHOOK_SECRET` in production to the signing secret for that endpoint.

## 7) Sanity checks

- Visit `/pricing/` and try upgrading (paid plan must have Price IDs)
- After successful checkout:
  - Your app redirects back to `/settings/billing/`
  - The subscription becomes active after the webhook arrives
- In Django admin, confirm `billing.Subscription` has:
  - `stripe_customer_id`
  - `stripe_subscription_id`
  - `status` = `active` or `trialing`

