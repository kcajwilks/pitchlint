---
name: design-with-hallmark
description: >
  Apply Hallmark to this Django SaaS starter’s marketing pages and light shell
  theming. Use after plans are Approved, when the user runs /design-with-hallmark,
  asks for marketing redesign, Hallmark audit/redesign/study, or implements the
  marketing-shell-design plan element. In this repo do not use Hallmark alone.
---

# Design With Hallmark

**Stack:** Vite + React SPA (`frontend/`). Hallmark restyles this app; it does not switch the framework to Next.js or anything else.

Orchestrates vendored [Hallmark](https://github.com/nutlope/hallmark) for this cookiecutter. Pack: [`.cursor/skills/references/pack.md`](../references/pack.md). Visual look may differ per app; process and shell IA stay the same.

**In this repository, never run Hallmark without this wrapper.** Hallmark’s own description fires on “build a new app”; greenfield here is `/new-saas-app`, not a Hallmark landing-page rebuild.

## Before you start

1. Announce: using `design-with-hallmark` + vendored `hallmark`.
2. Read [ui-surface-map.md](../references/ui-surface-map.md) and stay in scope.
3. Follow vendored `docs-plans` for any plan file updates.
4. Load `.cursor/skills/hallmark/SKILL.md`, then [THIS-REPO.md](../hallmark/THIS-REPO.md) (and Hallmark `references/` as Hallmark requires).

## Preconditions

- Prefer **Approved** (or Implementing) design plan in `docs/plans/` (slug like `marketing-shell-design`).
- If missing, create it at Pending Review via `plan-saas-from-starter` / `docs-plans` and **stop** for human approval unless the user explicitly asks to design now anyway.
- Work in **Agent mode**.

## Verb choice (ask once)

Ask which Hallmark verb to use; **recommend default build** if no reference site/screenshot:

| Verb | When |
|------|------|
| **build** (default) | Greenfield look from the product brief |
| **study** | User supplies URL or screenshot → DNA / optional `design.md`, then build |
| **redesign** | Keep copy + IA; new fingerprint |
| **audit** | Score only; punch list; no edits |

## Execution

1. Set design plan status to **Implementing** in the plan file and `PLANS.md`.
2. Run Hallmark with the chosen verb on **in-scope SPA surfaces only** (`frontend/src/tokens.css`, `index.css`, `HomePage.tsx`, pricing in `BillingPages.tsx`, `Layouts.tsx`). See ui-surface-map.
3. Do not rewrite Copilot (`AppCopilot` / `CopilotHost` / `core/copilot/`), DRF contracts, admin, settings IA, or Stripe webhooks unless a separate approved plan says so. Copilot work is `copilotkit-agno`.
4. Do not reintroduce Django product templates or Bootstrap.
5. When done: mark design plan **Complete** in both places; note outcome in `PLANS.md` Notes.

## Done criteria

- Marketing reflects the brief without generic AI-slop defaults (Hallmark gates)
- Shell tinted via tokens/CSS where appropriate
- Design plan tracker updated
- Out-of-scope surfaces untouched

## Related

[pack.md](../references/pack.md) · [ui-surface-map.md](../references/ui-surface-map.md) · [THIS-REPO.md](../hallmark/THIS-REPO.md) · [`docs-plans`](../docs-plans/SKILL.md) · [`new-saas-app`](../new-saas-app/SKILL.md) · [`copilotkit-agno`](../copilotkit-agno/SKILL.md) (do not Hallmark)
