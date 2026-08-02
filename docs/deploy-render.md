# Deploy on Render

This repo includes a `render.yaml` that deploys the app using Docker and provisions a Postgres database.

## 0) What you’ll deploy

- A web service running the `Dockerfile` (Gunicorn)
- A Postgres database managed by Render
- Static files served by WhiteNoise (collected at Docker build time)

## 1) Create the Render services

In Render:

- Create a **Blueprint** from this repo, or import the repo and apply `render.yaml`.

The blueprint provisions:

- Web service: `django-saas-starter`
- Database: `django-saas-db`

## 2) Set required environment variables

Render will generate or provide some env vars automatically via the blueprint, but you should confirm:

- `DJANGO_DEBUG` = `0`
- `DJANGO_SECRET_KEY` = (generated)
- `DATABASE_URL` = (from the Render Postgres database)

You should set these explicitly for your domain:

- `DJANGO_ALLOWED_HOSTS` = `yourdomain.com`

If you are using Stripe in production, also set:

- `STRIPE_SECRET_KEY`
- `STRIPE_PUBLIC_KEY`
- `STRIPE_WEBHOOK_SECRET`
- (Recommended) `STRIPE_PRICE_PRO_MONTHLY`, `STRIPE_PRICE_PRO_YEARLY`, etc. (see `docs/stripe.md`)

If you are using Google OAuth, also set:

- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`

## 3) Run migrations + seed plans

Render can run commands on deploy. You want to ensure these happen before serving traffic:

- `python manage.py migrate`
- `python manage.py seed_plans`

How you do this depends on how you prefer to operate:

- **Simple**: configure the service “Start Command” to run `migrate` then start Gunicorn
- **Better**: use a Render “Deploy Hook” / “Release Command” (preferred when available)

## 4) Configure Django Sites + Google SocialApp (if using Google login)

This starter uses `django.contrib.sites` with `SITE_ID=1`.

After deploy:

- Log into Django admin
- Confirm the `Site` domain/name match your production domain
- Create a `SocialApp` for Google and attach it to your `Site`

## 5) Add the Stripe webhook endpoint

In Stripe Dashboard:

- Add endpoint: `https://yourdomain.com/billing/webhook/`
- Subscribe to the subscription lifecycle events (see `docs/stripe.md`)
- Copy the signing secret into `STRIPE_WEBHOOK_SECRET` on Render

## 6) Smoke test checklist

- Visit `/` and `/pricing/`
- Sign up and log in
- Visit `/dashboard/` and `/settings/billing/`
- Start a Stripe checkout and confirm webhook updates local subscription status

## Notes

- The provided `render.yaml` currently sets `DJANGO_ALLOWED_HOSTS="*"` which is convenient but not ideal for production. Prefer a real domain allowlist.
- Email is configured to console output by default in `core/core/settings.py`. For production, set a real SMTP provider.

