# Starter map

Key paths for this Django SaaS cookiecutter (React SPA + Django REST). Pack: [../references/pack.md](../references/pack.md). Skill: [SKILL.md](SKILL.md). AI paths: [`copilotkit-agno`](../copilotkit-agno/SKILL.md).

## Project layout

```
core/                 # Django project (manage.py lives here)
  api/                # Auth + billing JSON endpoints, URL aggregate
  billing/            # Stripe plans, subscriptions, webhook
  copilot/            # CopilotKit runtime + thread/message models
  workspace/          # Sample domain: Project + AI brief (+ DRF in api.py)
  static/spa/         # Vite production build (npm run build)
  .env.example
frontend/             # Vite + React SPA (dev: npm run dev on :5173, proxies API)
docs/                 # Setup guides + docs/plans/
```

## API

| Piece | Path |
|-------|------|
| URLs | `/api/` → `core/api/urls.py` |
| Auth | `/api/csrf/`, `/api/me/`, `/api/auth/login|logout|signup/` |
| Projects | `/api/projects/` (ViewSet) + `generate-brief/` |
| Billing | `/api/billing/plans|subscription|checkout|portal/` |
| Webhook | `/billing/webhook/` (not under `/api/`) |
| Copilot | `/copilot/` (see skill `copilotkit-agno`) |

## Domain — workspace

| Piece | Path |
|-------|------|
| Models | `core/workspace/models.py` — `Project`, `ProjectBriefRun` |
| AI brief | `core/workspace/ai.py` |
| DRF | `core/workspace/api.py` |

## Auth

Session cookies + django-allauth. SPA uses JSON auth endpoints; Google OAuth still via `/accounts/` if configured.

## Frontend

| Piece | Path |
|-------|------|
| Entry | `frontend/src/main.tsx`, `App.tsx` |
| Copilot | `frontend/src/components/AppCopilot.tsx` (lazy-loads `CopilotHost.tsx`) |
| API client | `frontend/src/api/client.ts` |
| Dev | `cd frontend && npm run dev` (proxy to `:8000`) |
| Prod build | `npm run build` → `core/static/spa/` |

## Env vars

See `core/.env.example`. Copilot: `COPILOT_ENABLED=1` + `OPENAI_API_KEY`. Optional: `VITE_SITE_NAME`, `DJANGO_CSRF_TRUSTED_ORIGINS`.
