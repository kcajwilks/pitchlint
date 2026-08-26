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

## Start a new project from this starter

This repo is the **template**. Do **not** plan or build a product MVP inside `django-cookiecutter`. Clone into a **new directory**, open that folder in Cursor, then run the skills there.

### 1. Create the new repo location

Create an empty GitHub repo for your app first (example: `ai-api-explorer`), then:

```bash
# Ensure this starter (including .cursor/skills/) is pushed to GitHub first

git clone git@github.com:kcajwilks/django-cookiecutter.git ai-api-explorer
cd ai-api-explorer
git remote remove origin
git remote add origin git@github.com:kcajwilks/ai-api-explorer.git
git branch -M main
git push -u origin main
```

Replace `ai-api-explorer` with your project name. Open **that** folder in Cursor (new window), not this cookiecutter folder.

### 2. Environment

```bash
cp core/.env.example core/.env
```

Fill in new secrets (`DJANGO_SECRET_KEY`, `OPENAI_API_KEY` if you need AI, Stripe only if billing matters for MVP). **Do not** copy `core/.env` from the cookiecutter or another app.

Optional before planning: Quick start / Docker below so the starter runs. Planning does not require a live server.

### 3. Plan with skills (Agent mode)

| | |
|--|--|
| **Where** | The **new** project folder only |
| **Mode** | **Agent** |
| **Skill** | **`/new-saas-app`** (greenfield) |

Paste your MVP brief into that chat (problem, user flow, MVP features, boundaries).

Alternative (step-by-step): `/plan-saas-from-starter` only, then `/design-with-hallmark` after you approve plans.

What the agent should do:

1. Interview you (one question at a time) and map features onto this starter (auth, billing, workspace, CopilotKit/Agno).
2. Write **one plan per element** under `docs/plans/` + update `PLANS.md`, always including **`marketing-shell-design`**.
3. Stop at **Pending Review** — you approve; the agent must not implement yet.

### 4. After you approve

Still in **Agent** in the new project:

1. `/design-with-hallmark` (recommend **build** unless you have a reference URL/screenshot).
2. Implement remaining approved domain plans one at a time.

### Do not

- Run `/new-saas-app` or product planning inside `django-cookiecutter`
- Copy `core/.env` between apps
- Skip approval and jump to coding
- Ask Hallmark to redesign the whole authenticated shell (marketing + light shell tint only — see [ui-surface-map](./.cursor/skills/references/ui-surface-map.md))

Then continue with Quick start or Docker below if you have not already.

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

For a **new product**, follow [Start a new project from this starter](#start-a-new-project-from-this-starter) first (clone to a new directory, then run skills there).

In the product repo, use Cursor Agent skills to turn an MVP idea into reviewable work plans mapped onto this cookiecutter (auth, billing, workspace, CopilotKit/Agno), then Hallmark for marketing + light shell theming.

**Which skill?**
- **Greenfield ASAP:** `/new-saas-app` (checklist → plan → pause for approval → design → implement handoff).
- **Plan only / mid-project:** `/plan-saas-from-starter`.
- **Design only (after approval):** `/design-with-hallmark`.

Planning always emits a **design** plan element. You do not need to invoke `django-saas-starter` or `docs-plans` yourself unless you only need the starter map or are updating an existing plan outside a product kickoff.

**Which mode?** Use **Agent mode**. Skills must write `docs/plans/` and templates. Ask mode cannot write; Cursor Plan mode is for Cursor’s own plan UI, not this workflow. After plans are **Pending Review**, approve them, then design/implement in Agent mode.

1. Switch to **Agent mode**, then run **`/new-saas-app`** or **`/plan-saas-from-starter`**.
2. The agent loads [`.cursor/skills/django-saas-starter/`](./.cursor/skills/django-saas-starter/) and writes plans under [`docs/plans/`](./docs/plans/) via vendored [`docs-plans`](./.cursor/skills/docs-plans/) (tracker: [`docs/plans/PLANS.md`](./docs/plans/PLANS.md)).
3. Approve plans (including `marketing-shell-design`).
4. Run **`/design-with-hallmark`** (vendored [Hallmark](https://github.com/nutlope/hallmark); marketing + shell tint only — see [ui-surface-map](./.cursor/skills/references/ui-surface-map.md)).
5. Implement remaining approved domain plans.

| Skill | Where | Role |
|-------|--------|------|
| `new-saas-app` | [`.cursor/skills/new-saas-app/`](./.cursor/skills/new-saas-app/) | Meta kickoff (use for new apps) |
| `plan-saas-from-starter` | [`.cursor/skills/plan-saas-from-starter/`](./.cursor/skills/plan-saas-from-starter/) | Interview + emit plans (always includes design) |
| `design-with-hallmark` | [`.cursor/skills/design-with-hallmark/`](./.cursor/skills/design-with-hallmark/) | Hallmark marketing + light shell theme |
| `django-saas-starter` | [`.cursor/skills/django-saas-starter/`](./.cursor/skills/django-saas-starter/) | Starter capability map |
| `docs-plans` | [`.cursor/skills/docs-plans/`](./.cursor/skills/docs-plans/) | Plan file format + `PLANS.md` tracker |
| `hallmark` | [`.cursor/skills/hallmark/`](./.cursor/skills/hallmark/) | Vendored anti-slop design skill |

Shared refs: [`.cursor/skills/references/`](./.cursor/skills/references/). Starter map: [starter-map.md](./.cursor/skills/django-saas-starter/starter-map.md).

To refresh Hallmark later: `npx skills add nutlope/hallmark -y --copy` then copy into `.cursor/skills/hallmark/` (see `skills-lock.json`).

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
