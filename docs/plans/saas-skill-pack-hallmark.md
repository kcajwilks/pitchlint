---
status: Complete
owner: Jack Wilkins
created: 2026-08-26
updated: 2026-08-26
---

# SaaS skill pack + Hallmark (repeatable multi-app)

## Context

This cookiecutter is the template for spinning multiple SaaS apps ASAP (`git clone` → retarget remote → plan → build). It already ships `.cursor/skills/plan-saas-from-starter/` and `.cursor/skills/django-saas-starter/`, plus README guidance to use Agent mode and `/plan-saas-from-starter`. Plan I/O depends on the personal `docs-plans` skill; Hallmark ([nutlope/hallmark](https://github.com/nutlope/hallmark)) is not in the repo.

A grill-me session (2026-08-26) set the product intent: **same process + cookiecutter across apps; design may differ per app**; skill pack lives in the cookiecutter so every clone inherits it.

## Findings

- Project skills today: `plan-saas-from-starter`, `django-saas-starter` (+ `starter-map.md`) under `.cursor/skills/`.
- `docs-plans` exists personally (`~/.bob/skills/docs-plans`, `~/Dev/skills/prod/docs-plans`) but is **not** vendored; clones can lose plan formatting.
- Hallmark install options include `npx skills add nutlope/hallmark` or copying `SKILL.md` + `references/`; Cursor docs also mention a rules form. Nothing is vendored here yet.
- UI stack: Bootstrap Django templates for app shell; marketing at `home` / `pricing`; Copilot Vite bundle is separate from marketing chrome.
- Existing ASAP flow in README: clone → `/plan-saas-from-starter` → `docs/plans/` Pending Review → implement. No design step or meta kickoff skill.

## Root Cause

The gap is an incomplete, non-portable skill pack: planning format and anti-slop design are not guaranteed on clone, and there is no single kickoff path that sequences plan → approve → Hallmark (marketing + light shell theme) → implement.

## Proposed Solution

Grow `.cursor/skills/` in this cookiecutter into the repeatable pack. Do **not** lock a house visual brand (no shared `design.md`); Hallmark invents per app (or studies a reference when provided).

### Starter mapping

- **reuse** — `plan-saas-from-starter`, `django-saas-starter`, `docs/plans/` tracker, README kickoff section
- **extend** — `plan-saas-from-starter` (always emit a design plan element; point at design skill after approval)
- **new** — vendored `docs-plans`, vendored `hallmark`, `design-with-hallmark`, `new-saas-app`, shared references (plan template, kickoff checklist, UI surface map)

### Pack inventory

| Skill / ref | Role |
|-------------|------|
| `docs-plans` | Vendored plan format + `PLANS.md` rules |
| `hallmark` | Vendored [Hallmark](https://github.com/nutlope/hallmark) skill + `references/` |
| `design-with-hallmark` | Orchestrator: marketing + light shell theming; ask build vs study vs redesign (recommend build); update design plan in `docs/plans/` |
| `new-saas-app` | Meta: env checklist → `/plan-saas-from-starter` → pause for approval → `/design-with-hallmark` → implement handoff |
| `references/plan-template.md` | Canonical feature-plan section mapping |
| `references/kickoff-checklist.md` | Clone → env → migrate → seed → plan → design → implement |
| `references/ui-surface-map.md` | Hallmark may touch marketing + theme tokens; leave allauth/billing forms/dashboard IA |

### Pipeline (locked)

1. Clone starter, retarget remote (README).
2. Agent mode → `/new-saas-app` or `/plan-saas-from-starter`.
3. Planning always emits a design plan element (e.g. `marketing-shell-design`).
4. Human approves plans (Pending Review → Approved).
5. `/design-with-hallmark` implements the design plan (Hallmark default build unless study/redesign chosen).
6. Implement remaining approved domain plans.
7. Later UI changes: `hallmark audit` / `redesign` via the design orchestrator.

### UI scope (locked)

- Marketing pages + light shell theming (CSS variables / tokens to tint Bootstrap shell).
- Do not full-redesign dashboard/settings/allauth on every app.

## Implementation Steps

- [x] Vendor `docs-plans` into `.cursor/skills/docs-plans/` (copy from org skill; note sync with personal copy in README).
- [x] Vendor Hallmark into `.cursor/skills/hallmark/` (`SKILL.md` + `references/` from nutlope/hallmark; document update via `npx skills add nutlope/hallmark` / re-copy).
- [x] Add `.cursor/skills/references/plan-template.md`, `kickoff-checklist.md`, `ui-surface-map.md`.
- [x] Add `.cursor/skills/design-with-hallmark/SKILL.md` (scope B, verb ask+default build, docs-plans I/O for design plan).
- [x] Add `.cursor/skills/new-saas-app/SKILL.md` (meta sequence; Agent mode; pauses for human approval).
- [x] Update `plan-saas-from-starter` to always emit a design plan element and link `design-with-hallmark`.
- [x] Update root README (skill table, `/new-saas-app`, Hallmark step, vendored docs-plans) and `docs/README.md` if needed.
- [x] Smoke-check: skills discoverable under `.cursor/skills/`; no secrets; Hallmark refs present.

## Risks & Dependencies

- Vendoring Hallmark increases repo size and needs a periodic update ritual.
- Hallmark’s Cursor install docs mention `.cursor/rules/hallmark.mdc`; verify project skill discovery works with `.cursor/skills/hallmark/` (adjust if Cursor requires dual install).
- Over-scoping Hallmark into authenticated chrome would slow ASAP — enforce UI surface map.
- Personal `docs-plans` and vendored copy can drift — document which is source of truth for org vs this starter (recommendation: org personal remains canonical for non-cookiecutter repos; cookiecutter copy is freeze-for-clones, pull updates intentionally).

## Expected Outcome

After approval and implementation, cloning this starter yields a complete skill pack: one `/new-saas-app` path produces identically formatted `docs/plans/` work and a Hallmark-driven marketing + shell tint per product, without installing personal skills first. Time-to-first-approved-plan + design pass is a documented checklist, not ad hoc chat.

---
Owner: Jack Wilkins
Last reviewed: 2026-08-26
Review cadence: on change
