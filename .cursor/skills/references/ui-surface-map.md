# UI surface map (Hallmark scope)

Hallmark may change **marketing + light shell theming**. Do not full-redesign authenticated chrome on every app.

## In scope (touch freely)

| Surface | Paths |
|---------|--------|
| Marketing home | `core/templates/home.html`, related partials |
| Pricing | `core/templates/pricing.html` |
| Marketing / root bases | `core/templates/_base_marketing.html`, `_base_root.html` |
| Theme tokens / global CSS | `core/static/css/style.css` (CSS variables, colours, fonts) — tint shell to match marketing |
| Branding text | `SITE_NAME` / template brand strings as needed for the brief |

## Out of scope (leave unless a dedicated approved plan says otherwise)

| Surface | Paths |
|---------|--------|
| Auth (allauth) | `core/templates/account/`, `core/templates/allauth/`, `core/templates/socialaccount/` |
| Dashboard IA | `core/templates/dashboard.html`, sidebar/topbar structure in `_partials/` |
| Settings | `core/templates/settings/` |
| Billing flows | `core/templates/billing/` |
| Workspace CRUD chrome | `core/templates/workspace/` (content OK; don’t invent a new app shell) |
| Copilot React bundle | `frontend/`, `core/static/frontend/` |

## Rules

1. Prefer CSS variables on the existing Bootstrap shell over rewriting sidebar/settings markup.
2. Distinct product face lives on **marketing**; app shell stays cookiecutter-shaped and tinted.
3. If a brief needs a full app-shell redesign, that is a **separate** approved plan — not the default design element.
