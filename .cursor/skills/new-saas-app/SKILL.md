---
name: new-saas-app
description: >
  Meta kickoff for a new product cloned from this Django SaaS cookiecutter.
  Runs env checklist, plan-saas-from-starter, pauses for plan approval, then
  design-with-hallmark, then hands off to implement. Use when starting a new
  app ASAP, /new-saas-app, or greenfield kickoff on this starter.
---

# New SaaS App

Single entry path for greenfield ASAP. Keep using `/plan-saas-from-starter` or `/design-with-hallmark` alone when re-entering mid-project.

## Mode

**Agent mode only** (must write `docs/plans/` and templates).

## Sequence

1. Announce: using `new-saas-app`; plans via `docs-plans`; design via Hallmark after approval.
2. Follow `.cursor/skills/references/kickoff-checklist.md` sections 1–2 (clone/remote if needed, env). Skip clone steps if already in the target repo.
3. Run the full `/plan-saas-from-starter` workflow (read that skill and follow it). Ensure a **design** plan element is emitted.
4. **Stop for human approval.** List plan files and tell the user to approve in `docs/plans/` / `PLANS.md`. Do not self-approve. Do not implement domain or design yet.
5. When the user confirms plans are **Approved**, run `/design-with-hallmark` (read that skill).
6. Handoff: list remaining approved domain plans and recommend implementing them next (one plan at a time). Point at `django-saas-starter` / `starter-map.md` for paths.

## Rules

- Never skip the approval gate between plan and design/implement.
- Do not invent a parallel plan format — vendored `docs-plans` only.
- Design scope = marketing + light shell theming (`ui-surface-map.md`).

## Done criteria (kickoff)

- Checklist env items addressed or explicitly deferred
- Plans written at least through Pending Review (and Approved before design)
- Design pass complete after approval
- Clear next implementation targets listed
