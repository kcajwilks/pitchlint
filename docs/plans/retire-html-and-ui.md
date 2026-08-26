---
status: Pending Review
owner: Jack Wilkins
created: 2026-08-26
updated: 2026-08-26
---

# Retire HTML templates and Next.js ui/

## Context

Decision: full cutover; remove Next.js `ui/` from starter; Django admin remains the only server HTML UI.

## Findings

- Large `core/templates/` tree; `ui/` is a separate Next app; docs still mention both.

## Root Cause

Multiple frontends and leftover templates will confuse clones after SPA migration.

## Proposed Solution

After SPA routes cover marketing/app/billing/auth: delete product templates (keep admin if any custom); remove `ui/`; update Dockerfile/README/docs/skills; Django serves API + SPA static + admin + webhooks.

**Starter mapping**
- reuse: admin, webhook URLs
- extend: docs, Docker, skills maps
- new: none

## Implementation Steps

- [ ] Remove `ui/` directory and references
- [ ] Delete obsolete `core/templates/` product templates (keep minimal if any required by allauth fallback—prefer none)
- [ ] Update Dockerfile, README, `docs/*`, `.cursor/skills/django-saas-starter` + `starter-map.md`
- [ ] Confirm `/admin/`, `/api/`, `/billing/webhook/` still work

## Risks & Dependencies

- Do only after SPA parity for auth, shell, workspace, billing, marketing
- Depends on: all SPA feature plans + marketing-shell-design

## Expected Outcome

Starter has one frontend (`frontend/`), no Next.js app, no product Django templates.

---
Owner: Jack Wilkins
Last reviewed: 2026-08-26
Review cadence: on change
