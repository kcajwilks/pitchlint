---
name: design-with-hallmark
description: >
  Apply Hallmark to this Django SaaS starter’s marketing pages and light shell
  theming. Use after plans are Approved, when the user runs /design-with-hallmark,
  asks for marketing redesign, Hallmark audit/redesign/study, or implements the
  marketing-shell-design plan element.
---

# Design With Hallmark

Orchestrates [Hallmark](https://github.com/nutlope/hallmark) for this cookiecutter. Visual look may differ per app; process and shell IA stay the same.

## Before you start

1. Announce: using `design-with-hallmark` + vendored `hallmark`.
2. Read `.cursor/skills/references/ui-surface-map.md` and stay in scope.
3. Follow vendored `docs-plans` for any plan file updates.
4. Load `.cursor/skills/hallmark/SKILL.md` (and its `references/` as Hallmark requires).

## Preconditions

- Prefer **Approved** (or Implementing) design plan in `docs/plans/` (slug like `marketing-shell-design`).
- If missing, create it at Pending Review and **stop** for human approval unless the user explicitly asks to design now anyway.
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
2. Run Hallmark with the chosen verb on **in-scope** surfaces only (marketing templates + theme tokens / `core/static/css/style.css`).
3. Do not rewrite allauth, settings, billing forms, or dashboard IA unless a separate approved plan says so.
4. When done: mark design plan **Complete** in both places; note outcome in `PLANS.md` Notes.

## Done criteria

- Marketing reflects the brief without generic AI-slop defaults (Hallmark gates)
- Shell tinted via tokens/CSS where appropriate
- Design plan tracker updated
- Out-of-scope templates untouched
