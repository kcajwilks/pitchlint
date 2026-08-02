# Django SaaS Starter (AI-ready shell)

A Django starter for building AI SaaS products with:

- modern Bootstrap 5.3 UI (Stripe-style light + dark theme)
- django-allauth authentication (email/password + Google)
- dashboard app shell (collapsible sidebar + top bar)
- settings IA (`/settings/profile`, `/settings/account`, `/settings/billing`)
- Stripe billing integration (checkout, portal, webhook)

## Prerequisites

- Python 3.9+
- pip

A virtual environment is recommended.

## Quick start

From the repo root:

```bash
cd core
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # optional; needed to log in
python manage.py runserver
```

## Docker + Postgres (recommended dev setup)

From the repo root:

```bash
docker compose up --build
```

Then open:

- **Home**: http://127.0.0.1:8000/

## AI quickstart (Agno)

1. Set `OPENAI_API_KEY` in `core/.env` (copy from `core/.env.example`).
2. Create a project in **Workspace** and click **Generate AI brief**.

## Environment variables (.env)

The project supports loading environment variables from `core/.env` (via `python-dotenv`).

Copy the example file and fill in your Stripe keys:

```bash
cp core/.env.example core/.env
```

## Stripe webhooks (local development)

To forward Stripe events to your local webhook endpoint:

```bash
stripe listen --forward-to http://127.0.0.1:8000/billing/webhook/
```

Then copy the printed webhook secret (`whsec_...`) into `core/.env` as `STRIPE_WEBHOOK_SECRET`.

Then open:

- **Home**: http://127.0.0.1:8000/
- **Login**: http://127.0.0.1:8000/accounts/login/
- **Pricing**: http://127.0.0.1:8000/pricing/
- **Dashboard** (after login): http://127.0.0.1:8000/dashboard/
- **Settings** (after login): http://127.0.0.1:8000/settings/profile/
- **Admin**: http://127.0.0.1:8000/admin/

## Seed default plans

Create the default plan catalog (Free, Pro, Business):

```bash
cd core
python3 manage.py seed_plans
```

`seed_plans` reads optional Stripe price IDs from:

- `STRIPE_PRICE_PRO_MONTHLY`
- `STRIPE_PRICE_PRO_YEARLY`
- `STRIPE_PRICE_BUSINESS_MONTHLY`
- `STRIPE_PRICE_BUSINESS_YEARLY`

## Project structure

- **`core/`** — Project root; run `manage.py` from here. Contains the project package, apps, templates, and static files.
- **`core/core/`** — Project config: `settings.py`, root `urls.py`, home view in `views.py`.
- **`core/dashboard/`** — Dashboard and settings views for authenticated users.
- **`core/billing/`** — Billing models, Stripe services, views, webhook handling, and `seed_plans` command.
- **`core/templates/`** — Marketing and app shell templates, account/auth templates, settings pages.
- **`core/static/`** — Theme CSS and small JS helpers (`theme.js`, `sidebar.js`, `pricing.js`).

## Plan a SaaS on this starter

Use Cursor Agent skills to turn a product idea into reviewable work plans mapped onto this cookiecutter (auth, billing, workspace, CopilotKit/Agno).

1. In Agent chat, run **`/plan-saas-from-starter`** (interview → map elements → write plans).
2. The agent loads [`.cursor/skills/django-saas-starter/`](./.cursor/skills/django-saas-starter/) for what the starter already ships.
3. Plans are written under [`docs/plans/`](./docs/plans/) using the `docs-plans` standard (one file per application element + tracker [`docs/plans/PLANS.md`](./docs/plans/PLANS.md)).
4. New plans land at **Pending Review** — approve before implementation.

| Skill | Where | Role |
|-------|--------|------|
| `plan-saas-from-starter` | [`.cursor/skills/plan-saas-from-starter/`](./.cursor/skills/plan-saas-from-starter/) | Interview + emit plans |
| `django-saas-starter` | [`.cursor/skills/django-saas-starter/`](./.cursor/skills/django-saas-starter/) | Starter capability map |
| `docs-plans` | Personal skill set | Plan file format + `PLANS.md` tracker |

Starter map details: [`.cursor/skills/django-saas-starter/starter-map.md`](./.cursor/skills/django-saas-starter/starter-map.md).

## Docs

Step-by-step guides live in [`docs/`](./docs/):

- Getting started: [`docs/getting-started.md`](./docs/getting-started.md)
- Stripe setup: [`docs/stripe.md`](./docs/stripe.md)
- Deploy on Render: [`docs/deploy-render.md`](./docs/deploy-render.md)
- CopilotKit + Agno (bolt-on): [`docs/copilotkit-bolton.md`](./docs/copilotkit-bolton.md)
- Work plans tracker: [`docs/plans/PLANS.md`](./docs/plans/PLANS.md)

## URLs

| URL | Description |
|-----|-------------|
| `/` | Public marketing home page (hero + how-it-works + pricing preview). |
| `/pricing/` | Full pricing page with monthly/yearly toggle. |
| `/accounts/login/` | Login form (email/password + Google). |
| `/accounts/signup/` | Sign-up form (email/password + Google). |
| `/dashboard/` | Dashboard home (usage tiles + upgrade CTA). |
| `/settings/profile/` | Profile settings. |
| `/settings/account/` | Account/security settings and account deletion. |
| `/settings/billing/` | Billing settings and plan selection. |
| `/billing/webhook/` | Stripe webhook endpoint. |
| `/admin/` | Django admin site. |

## Settings

- **`SITE_NAME`** — Branding text used in templates (default: `Acme AI`).
- **`LOGOUT_REDIRECT_URL`** — `'home'`.
- **`ACCOUNT_LOGIN_METHODS`** — `{'email'}`.
- **`SOCIALACCOUNT_PROVIDERS`** — Google provider enabled.
- **Theme toggle** — User menu provides `system/light/dark` and persists in `localStorage`.

## Google OAuth setup (allauth)

Add these to `core/.env`:

```env
GOOGLE_CLIENT_ID=your_google_oauth_client_id
GOOGLE_CLIENT_SECRET=your_google_oauth_client_secret
```

Then create/configure a Google `SocialApp` in Django admin and attach it to your site.

## Notes on starter scope

- The previous example Notes module has been removed.
- This starter now focuses on reusable SaaS chrome; add product-specific AI features in the `Workspace` area.
