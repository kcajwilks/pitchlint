# Starter map

Key paths for this Django SaaS cookiecutter. Read on demand from `django-saas-starter`.

## Project layout

```
core/                 # Django project (manage.py lives here)
  billing/            # Stripe plans, subscriptions, webhook
  copilot/            # CopilotKit runtime + thread/message models
  dashboard/          # Dashboard home + settings views
  workspace/          # Sample domain: Project + AI brief
  templates/          # Django templates (app shell + marketing)
  static/             # CSS/JS; frontend/ = Vite Copilot build output
  .env.example        # Env template
frontend/             # Vite + React CopilotKit UI (builds into core/static/frontend)
ui/                   # Separate Next.js app (not the Django shell)
agent/                # Standalone Agno agent package
docs/                 # Setup guides + docs/plans/
```

## Domain — workspace

| Piece | Path |
|-------|------|
| Models | `core/workspace/models.py` — `Project`, `ProjectBriefRun` |
| AI brief | `core/workspace/ai.py` |
| Views | `core/workspace/views.py` |
| URLs | `core/workspace/urls.py` — list/create/detail/edit/delete + `generate-brief` |
| Templates | `core/templates/workspace/` |

Primary domain object today: `Project` (owner FK, name, description, `ai_brief`).

## Billing

| Piece | Path |
|-------|------|
| Models | `core/billing/models.py` — `Plan`, `Subscription`, `BillingEvent` |
| Services | `core/billing/services.py` — Stripe customer, checkout, portal, webhook sync |
| Gate | `core/billing/permissions.py` — `subscription_required`, `SubscriptionRequiredMixin` |
| Seed | `python manage.py seed_plans` |
| Templates | `core/templates/billing/`, settings billing via dashboard |
| Guide | `docs/stripe.md` |

## Auth and settings

| Piece | Path |
|-------|------|
| Allauth | mounted at `/accounts/` |
| Settings URLs | `core/dashboard/settings_urls.py` — profile, account, billing, delete |
| Settings templates | `core/templates/settings/` |
| Google OAuth env | `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` |

## Copilot / Agno

| Piece | Path |
|-------|------|
| Models | `core/copilot/models.py` — `CopilotThread`, `CopilotMessage` |
| Agent | `core/copilot/ai.py` |
| Views/URLs | `core/copilot/views.py`, `core/copilot/urls.py` |
| Template partial | `core/templates/_partials/_copilot.html` |
| Vite entry | `frontend/src/copilot.tsx` |
| Vite outDir | `core/static/frontend/` (`copilot.js`, `copilot.css`, chunks) |
| Guides | `docs/copilotkit.md`, `docs/copilotkit-bolton.md` |

Build: `cd frontend && npm install && npm run build` (Docker builds this in the image).

## Env vars (from `core/.env.example`)

- Stripe: `STRIPE_SECRET_KEY`, `STRIPE_PUBLIC_KEY`, `STRIPE_WEBHOOK_SECRET`
- Django: `DJANGO_DEBUG`, `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `SITE_NAME`
- DB: `DATABASE_URL` (Postgres in Docker/prod; SQLite local default)
- AI: `OPENAI_API_KEY`, `AGNO_MODEL_ID`
- Copilot: `COPILOT_ENABLED`
- OAuth: `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`

## Templates / static shell

| Piece | Path |
|-------|------|
| Base layouts | `core/templates/_base_*.html` |
| Partials | `core/templates/_partials/` (sidebar, topbar, copilot, theme) |
| Marketing | `home.html`, `pricing.html` |
| App CSS/JS | `core/static/css/`, `core/static/js/` |

## Deploy

| Piece | Path |
|-------|------|
| Compose | `docker-compose.yml` |
| Dockerfile | multi-stage: Node frontend build → Python + collectstatic |
| Render | `render.yaml`, `docs/deploy-render.md` |
