---
status: Pending Review
owner: Jack Wilkins
created: 2026-08-26
updated: 2026-08-26
---

# React app shell (replace HTML chrome)

## Context

Dashboard, settings chrome, marketing routes must move to React. Styling: plain CSS + Hallmark tokens (no Bootstrap in SPA). Design look deferred to `marketing-shell-design` / Hallmark after approval.

## Findings

- Shell templates: `_base_*.html`, `_partials/`, `dashboard.html`, `settings/`, `home.html`, `pricing.html`.
- `ui-surface-map.md` still names Django templates as Hallmark targets.

## Root Cause

Product chrome is server-rendered Bootstrap HTML, incompatible with the SPA decision.

## Proposed Solution

React Router layout: marketing layout + authenticated app layout (nav, outlet). Routes for home, pricing, dashboard, settings placeholders. Structural CSS only until Hallmark design pass; ship empty/minimal tokens.css.

**Starter mapping**
- reuse: URL IA concepts (`/dashboard`, `/settings`, `/pricing`)
- extend: `frontend/src/` into app structure
- new: router, layouts, pages (thin)

## Implementation Steps

- [ ] Add react-router; layouts for marketing vs app
- [ ] Port route map: `/`, `/pricing`, `/dashboard`, `/settings/*`
- [ ] Minimal `tokens.css` + global CSS (pre-Hallmark)
- [ ] Update skills `ui-surface-map.md` to React paths under `frontend/src/`

## Risks & Dependencies

- Hallmark must target React files, not removed templates
- Depends on: spa-auth-allauth; design plan for visuals

## Expected Outcome

Authenticated user sees a React shell with navigable placeholder pages; no Bootstrap dependency for those routes.

---
Owner: Jack Wilkins
Last reviewed: 2026-08-26
Review cadence: on change
