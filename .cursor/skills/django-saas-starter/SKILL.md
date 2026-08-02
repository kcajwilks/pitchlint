---
name: django-saas-starter
description: >
  Capability map and extension rules for this Django SaaS cookiecutter (allauth,
  billing/Stripe, workspace, CopilotKit/Agno, Bootstrap shell). Use when planning
  or building features on this starter, deciding reuse vs new app, wiring billing
  or AI, or when plan-saas-from-starter needs the project inventory.
---

# Django SaaS Starter

Project reference for this cookiecutter. For product kickoff planning, also use `plan-saas-from-starter`. All work plans go through `docs-plans` under `docs/plans/`.

## Already provided

| Area | What you get |
|------|----------------|
| Auth | django-allauth (email/password + Google); settings at `/settings/*` |
| Shell UI | Bootstrap 5.3 light/dark; dashboard + marketing templates in `core/templates/` |
| Billing | `core/billing/` — Plan/Subscription, Stripe checkout/portal/webhook, `seed_plans` |
| Domain | `core/workspace/` — `Project` CRUD + AI brief generation |
| AI | `core/copilot/` + Vite bundle → `core/static/frontend/`; Agno agents; `COPILOT_ENABLED` |
| Deploy | Docker Compose, Render (`docs/deploy-render.md`) |

## Extension rules

1. Prefer **extend** `workspace` (or rename the domain) over inventing a parallel CRUD shell.
2. New bounded context → new Django app under `core/`.
3. Paid features → `billing.permissions` / `has_active_subscription`; do not reinvent Stripe.
4. Chat UI → CopilotKit path; structured AI jobs → Agno + `output_schema` (see `.cursorrules`).
5. App shell → Django templates; `frontend/` only for the embedded Copilot Vite bundle.
6. Plans → `docs/plans/` via the `docs-plans` skill only.

## URL mounts

From `core/core/urls.py`:

- `/accounts/` — allauth
- `/dashboard/` — app shell home
- `/workspace/` — projects
- `/settings/` — profile, account, billing settings
- `/billing/` — Stripe flows + webhook
- `/copilot/` — CopilotKit runtime

## Progressive disclosure

For concrete paths (models, env vars, templates, build), see [starter-map.md](starter-map.md).
