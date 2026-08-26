# UI surface map (Hallmark scope)

Pack: [pack.md](pack.md). Run via [`design-with-hallmark`](../design-with-hallmark/SKILL.md), not Hallmark alone. Copilot chrome is [`copilotkit-agno`](../copilotkit-agno/SKILL.md) — out of scope here.

Hallmark may change **marketing + light shell theming** in the React SPA. Do not full-redesign authenticated IA on every app.

## In scope (touch freely)

| Surface | Paths |
|---------|--------|
| Tokens | `frontend/src/tokens.css` |
| Global styles | `frontend/src/index.css` |
| Marketing | `frontend/src/pages/HomePage.tsx`, `frontend/src/pages/BillingPages.tsx` (pricing) |
| Chrome layouts | `frontend/src/layouts/Layouts.tsx` |
| Branding | `VITE_SITE_NAME` / `SITE_NAME` |

## Out of scope (leave unless a dedicated approved plan says otherwise)

| Surface | Paths |
|---------|--------|
| Django admin | `/admin/` |
| Stripe webhook | `/billing/webhook/` |
| API contracts | `core/api/`, DRF serializers — design may not break JSON shapes |
| Copilot runtime | `core/copilot/`, `frontend/src/components/AppCopilot.tsx`, `CopilotHost.tsx` |

## Rules

1. Prefer CSS variables on the existing React shell over inventing a second navigation IA.
2. Distinct product face lives on **marketing**; app shell stays cookiecutter-shaped and tinted.
3. If a brief needs a full app-shell redesign, that is a **separate** approved plan — not the default design element.
