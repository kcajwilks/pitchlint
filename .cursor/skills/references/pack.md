# Skill pack (this cookiecutter)

Load this file before inventing a stack, a second frontend, or skipping approval.

## Stack (fixed)

This cookiecutter is always:

- **Django** in `core/` (DRF under `/api/`, allauth sessions, Stripe webhook, Copilot runtime)
- **Vite + React SPA** in `frontend/` (one app; Hallmark tokens; CopilotKit sidebar)

Never introduce FastAPI, Next.js, a second frontend, or Django product templates. CopilotKit UI lives in the existing SPA; Agno runs inside Django `core/copilot/`.

## Sequence

```
/new-saas-app
  → kickoff-checklist (env)
  → /plan-saas-from-starter
       → docs-plans + plan-template.md
       → django-saas-starter (+ starter-map.md)
       → always emit marketing-shell-design
  → human sets 🟢 Approved (never self-approve)
  → /design-with-hallmark
       → ui-surface-map.md
       → vendored hallmark (scope only)
  → implement one approved plan at a time
       → django-saas-starter for paths
       → copilotkit-agno if chat/agents/structured AI
       → docs-plans status 🔨 then ✅
```

Mid-project: `/plan-saas-from-starter` or `/design-with-hallmark` alone. Do not re-run greenfield kickoff inside `django-cookiecutter` itself — clone first (README).

## Who owns what

| Skill | Owns | Does not own |
|-------|------|----------------|
| `new-saas-app` | Kickoff order + approval gate | Domain code, Hallmark pixels |
| `plan-saas-from-starter` | Interview + one plan per element | Implementation, design pixels |
| `docs-plans` | `docs/plans/*.md` + `PLANS.md` format | Product architecture |
| `django-saas-starter` | Inventory, reuse vs new app | CopilotKit API details |
| `design-with-hallmark` | Marketing + light shell theming | Copilot, API, admin, Stripe webhook |
| `hallmark` | Anti-slop craft (vendored) | This repo’s routes/IA — wrapper decides scope |
| `copilotkit-agno` | Chat UI + Agno tools/jobs | Marketing redesign, billing, new SPA |

## Hard no

- FastAPI (including AgentOS `get_app()`, SQLModel, fastapi-users)
- Next.js `ui/`, extra Vite app, `@copilotkit/runtime` in `frontend/`
- Django **product** templates / Bootstrap product UI
- Hallmark on Copilot, DRF contracts, admin, or `/billing/webhook/`
- Committing `core/static/spa/`
- Implementing before **Approved** unless the user explicitly says to implement now
- Self-approving plans

## Shared files

- Paths: `.cursor/skills/django-saas-starter/starter-map.md`
- Design scope: `.cursor/skills/references/ui-surface-map.md`
- Plan shape: `.cursor/skills/references/plan-template.md`
- Kickoff env: `.cursor/skills/references/kickoff-checklist.md`
- Hallmark repo overlay: `.cursor/skills/hallmark/THIS-REPO.md` (re-apply after Hallmark refresh)

Always-apply Cursor rule: `.cursor/rules/saas-skill-pack.mdc` (locks Django + Vite + React; ignores FastAPI Copilot samples).
