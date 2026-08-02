# Getting started

This guide gets you running locally with authentication + dashboard + Stripe billing pages.

## Prerequisites

- Python 3.9+
- (Recommended) Docker Desktop for the Postgres dev setup
- Stripe CLI (optional, for local webhooks)

## 1) Clone and create your env file

From the repo root:

```bash
cp core/.env.example core/.env
```

Edit `core/.env` and set at least:

- `DJANGO_SECRET_KEY` (any random string is fine for local dev)
- `DJANGO_ALLOWED_HOSTS` (defaults are fine for localhost)

If you want billing pages + checkout to work locally, also set:

- `STRIPE_SECRET_KEY`
- `STRIPE_PUBLIC_KEY`
- `STRIPE_WEBHOOK_SECRET` (after `stripe listen`, see Stripe guide)

## 2) Run with Docker + Postgres (recommended)

From the repo root:

```bash
docker compose up --build
```

The container startup runs:

- `python manage.py migrate`
- `python manage.py seed_plans`
- `python manage.py runserver 0.0.0.0:8000`

Open:

- Home: http://127.0.0.1:8000/
- Login: http://127.0.0.1:8000/accounts/login/
- Pricing: http://127.0.0.1:8000/pricing/
- Dashboard: http://127.0.0.1:8000/dashboard/
- Settings: http://127.0.0.1:8000/settings/profile/
- Admin: http://127.0.0.1:8000/admin/

## 3) Run without Docker (SQLite fallback)

From the repo root:

```bash
cd core
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_plans
python manage.py runserver
```

If you *do* want Postgres without Docker, set `DATABASE_URL` in `core/.env`.

## 4) Create an admin user (optional)

If you want to use Django admin:

```bash
cd core
python manage.py createsuperuser
```

Then visit http://127.0.0.1:8000/admin/

## 5) Next steps (typical SaaS setup)

- Configure Stripe products/prices + webhooks: see [`stripe.md`](./stripe.md)
- Deploy to a real domain: see [`deploy-render.md`](./deploy-render.md)
- Decide how you want to gate features:
  - **Simple**: require an active subscription for paid features
  - **Advanced**: use plan “features” / limits per plan (seats, quotas, feature flags)

