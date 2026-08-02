---
name: plan-saas-from-starter
description: >
  Interview the user about a SaaS product idea and map application elements onto a
  Django SaaS cookiecutter (auth, billing, workspace, CopilotKit/Agno). Writes one
  reviewable plan per element under docs/plans/ using the docs-plans standard.
  Use when planning a SaaS on this starter, kicking off a product, mapping
  application elements, or deciding what to build vs reuse on the cookiecutter.
---

# Plan SaaS From Starter

Turn a product idea into reviewable `docs/plans/` entries mapped onto the Django SaaS cookiecutter.

## Before you start

1. Announce: you are using `plan-saas-from-starter`, and plan files will follow `docs-plans`.
2. Read and follow the `docs-plans` skill for all plan I/O (file layout, `PLANS.md`, status values, anti-patterns). Do not invent a parallel planning format.
3. Load the project skill `django-saas-starter` if present (`.cursor/skills/django-saas-starter/`). Read `starter-map.md` when you need concrete paths. If the project skill is missing, briefly inventory `core/*/apps.py` and top-level urls instead.

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
2. If `docs/plans/` or `docs/plans/PLANS.md` is missing, create them (empty tracker table per docs-plans).
3. For each element, write `docs/plans/<slug>.md` and add/update the row in `PLANS.md`.
4. Slugs: kebab-case describing the problem/element (e.g. `workspace-domain-model`, `billing-entitlement-exports`).
5. Set status to **Pending Review** in both places. **Do not implement** and do not self-approve.

Owner: use the repo’s usual owner if known; otherwise the current user / agent name the project already uses in docs-plans examples.

## Feature-plan section mapping

Keep every docs-plans required heading. Interpret them for greenfield SaaS features:

| Section | Meaning for SaaS elements |
|---------|---------------------------|
| Context | Product intent for this element; who needs it |
| Findings | What the starter already provides (cite apps/paths from `django-saas-starter`) |
| Root Cause | The gap — why this element is not already done |
| Proposed Solution | How to extend the starter; include **Starter mapping** bullets: `reuse` / `extend` / `new app` |
| Implementation Steps | Checklist; mark schema work `(requires migration)` |
| Risks & Dependencies | Other element plans, Stripe, Copilot, deploy |
| Expected Outcome | User-visible MVP criterion for this element |

## Starter mapping rules (quick)

- Prefer **extend** `workspace` (or rename the domain) over a parallel CRUD shell
- New bounded context → **new app** under `core/`
- Paid features → billing permissions / `has_active_subscription`; do not reinvent Stripe
- Chat UI → CopilotKit path; structured AI jobs → Agno + `output_schema`
- App shell → Django templates; `frontend/` only for the embedded Copilot Vite bundle

## Done criteria

- Interview complete for MVP elements
- One plan file per element + `PLANS.md` updated
- All new plans at Pending Review
- No implementation started
