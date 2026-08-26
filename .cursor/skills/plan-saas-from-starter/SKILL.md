---
name: plan-saas-from-starter
description: >
  Interview the user about a SaaS product idea and map application elements onto a
  Django SaaS cookiecutter (auth, billing, workspace, CopilotKit/Agno). Writes one
  reviewable plan per element under docs/plans/ using the docs-plans standard.
  Always emits a marketing-shell-design plan for design-with-hallmark. Use when
  planning a SaaS on this starter, kicking off a product, mapping application
  elements, or deciding what to build vs reuse on the cookiecutter.
---

# Plan SaaS From Starter

**Stack:** Django + DRF + Vite + React. Map the product onto this starter; never plan a FastAPI or Next.js rewrite.

Turn a product idea into reviewable `docs/plans/` entries mapped onto the Django SaaS cookiecutter.

## Before you start

1. Announce: you are using `plan-saas-from-starter`. Follow [pack.md](../references/pack.md).
2. Read and follow the vendored `docs-plans` skill (`.cursor/skills/docs-plans/`) for all plan I/O. Do not invent a parallel planning format. See also `.cursor/skills/references/plan-template.md`.
3. Load `django-saas-starter` (`.cursor/skills/django-saas-starter/`). Read `starter-map.md` when you need concrete paths. If the project skill is missing, briefly inventory `core/*/apps.py` and top-level urls instead.
4. If the MVP includes chat or structured AI, cite `copilotkit-agno` in that element’s Findings — Django runtime + CopilotKit in the existing SPA.

## Interview

Interview like `grill-me`: **one question at a time**, with your recommended answer each time. Resolve dependencies before moving on. Explore the codebase instead of asking when the answer is already in the repo.

Decision order:

1. Problem / ICP / core job-to-be-done
2. Primary domain object (what replaces or extends `workspace.Project`)
3. Auth beyond allauth (teams/orgs? roles?)
4. Billing gates (which features are paid; plan names)
5. AI surface (Copilot chat vs Agno structured jobs vs none)
6. Must-have MVP screens vs later

Stop interviewing when you have shared understanding of the MVP application elements.

## Decompose and write plans

After the interview:

1. Split work into **one plan file per application element** (docs-plans: no multi-unrelated mega-plan). Typical elements: domain model, CRUD/UI, billing entitlement, AI agent/tooling, integrations.
2. **Always** emit a design plan element (slug e.g. `marketing-shell-design`) for marketing + light shell theming. Implementation of that plan is `/design-with-hallmark` after approval — cite `.cursor/skills/references/ui-surface-map.md` in Findings/Proposed Solution.
3. If `docs/plans/` or `docs/plans/PLANS.md` is missing, create them (empty tracker table per docs-plans).
4. For each element, write `docs/plans/<slug>.md` and add/update the row in `PLANS.md`.
5. Slugs: kebab-case describing the problem/element (e.g. `workspace-domain-model`, `billing-entitlement-exports`, `marketing-shell-design`).
6. Set status to **Pending Review** in both places. **Do not implement** and do not self-approve.

Owner: use the repo’s usual owner if known; otherwise the current user / agent name the project already uses in docs-plans examples.

## Feature-plan section mapping

Keep every docs-plans required heading. Interpret them for greenfield SaaS features (see `references/plan-template.md`):

| Section | Meaning for SaaS elements |
|---------|---------------------------|
| Context | Product intent for this element; who needs it |
| Findings | What the starter already provides (cite apps/paths from `django-saas-starter`) |
| Root Cause | The gap — why this element is not already done |
| Proposed Solution | How to extend the starter; include **Starter mapping** bullets: `reuse` / `extend` / `new app` |
| Implementation Steps | Checklist; mark schema work `(requires migration)` |
| Risks & Dependencies | Other element plans, Stripe, Copilot, deploy, design plan |
| Expected Outcome | User-visible MVP criterion for this element |

## Starter mapping rules (quick)

- Prefer **extend** `workspace` (or rename the domain) over a parallel CRUD shell
- New bounded context → **new app** under `core/`
- Paid features → billing permissions / `has_active_subscription`; do not reinvent Stripe
- Chat UI → CopilotKit path; structured AI jobs → Agno + `output_schema` (implement via `.cursor/skills/copilotkit-agno/`)
- App shell → React SPA in `frontend/`; do not reintroduce product Django templates
- Marketing look → `/design-with-hallmark` after approval (not ad hoc CSS in domain plans)

## Done criteria

- Interview complete for MVP elements
- One plan file per element including **design** + `PLANS.md` updated
- All new plans at Pending Review
- No implementation started (handoff: `/design-with-hallmark` after approval, then `django-saas-starter` / `copilotkit-agno`)

## Related

[pack.md](../references/pack.md) · [`new-saas-app`](../new-saas-app/SKILL.md) · [`docs-plans`](../docs-plans/SKILL.md) · [`django-saas-starter`](../django-saas-starter/SKILL.md) · [`design-with-hallmark`](../design-with-hallmark/SKILL.md) · [`copilotkit-agno`](../copilotkit-agno/SKILL.md)
