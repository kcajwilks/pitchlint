---
name: django-saas-starter
description: >
  Capability map and extension rules for this Django SaaS cookiecutter (React SPA,
  DRF, allauth sessions, billing/Stripe, workspace, CopilotKit/Agno). Use when
  planning or building features on this starter, deciding reuse vs new app, wiring
  billing or AI, or when plan-saas-from-starter needs the project inventory.
---

# Django SaaS Starter

**Stack:** Django + DRF in `core/`, Vite + React SPA in `frontend/`. Never FastAPI or a second frontend.

Inventory for this cookiecutter. Pack: [`.cursor/skills/references/pack.md`](../references/pack.md). Greenfield: `/new-saas-app`. Planning: `/plan-saas-from-starter`. Design after approval: `/design-with-hallmark`. AI: [`copilotkit-agno`](../copilotkit-agno/SKILL.md). Plans: vendored `docs-plans`.

## Already provided

| Area | What you get |
|------|----------------|
| Frontend | Vite + React SPA in `frontend/` (plain CSS + Hallmark tokens) |
| API | Django REST framework under `/api/` (session auth) |
| Auth | django-allauth + JSON login/signup/me; Google via `/accounts/` |
| Billing | `core/billing/` + `/api/billing/*`; Stripe webhook |
| Domain | `workspace.Project` CRUD + AI brief via API |
| AI | `core/copilot/` + `AppCopilot` sidebar in SPA; Agno + workspace tools |
| Deploy | Docker Compose, Render; SPA build copied to `core/static/spa` |

## Extension rules

1. Prefer **extend** `workspace` (or rename the domain) over inventing a parallel CRUD shell.
2. New bounded context → new Django app under `core/` + DRF routes under `/api/`.
3. Paid features → billing permissions / `has_active_subscription`; do not reinvent Stripe.
4. Chat UI → CopilotKit in the SPA; structured AI jobs → Agno + `output_schema`. Load [`.cursor/skills/copilotkit-agno/`](../copilotkit-agno/SKILL.md) when implementing AI.
5. UI → React in `frontend/`; do not reintroduce product Django templates.
6. Plans → `docs/plans/` via the `docs-plans` skill only.

## URL mounts

- `/api/` — REST API
- `/accounts/` — allauth (OAuth redirects)
- `/billing/webhook/` — Stripe
- `/copilot/` — CopilotKit runtime
- `/admin/` — Django admin
- `/*` — React SPA

## Progressive disclosure

For concrete paths, see [starter-map.md](starter-map.md). For CopilotKit/Agno extension, see [`copilotkit-agno`](../copilotkit-agno/SKILL.md).

## Related

[pack.md](../references/pack.md) · [`plan-saas-from-starter`](../plan-saas-from-starter/SKILL.md) · [`docs-plans`](../docs-plans/SKILL.md) · [`design-with-hallmark`](../design-with-hallmark/SKILL.md)
