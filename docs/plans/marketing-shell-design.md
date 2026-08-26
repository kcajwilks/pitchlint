---
status: Pending Review
owner: Jack Wilkins
created: 2026-08-26
updated: 2026-08-26
---

# Marketing + shell design (Hallmark)

## Context

SPA uses plain CSS + Hallmark tokens. Visual identity for marketing and light shell theming comes from Hallmark after plans are approved (`/design-with-hallmark`).

## Findings

- `design-with-hallmark` + vendored `hallmark` exist; `ui-surface-map.md` still lists Django templates.
- Genre for this starter brief fits **modern-minimal** (SaaS / API platform).

## Root Cause

No React-targeted design pass yet; shell will ship structurally first.

## Proposed Solution

After approval, run `/design-with-hallmark` (ask build vs study vs redesign; recommend **build**). Scope: marketing pages + light shell theming in `frontend/src` + `tokens.css`. Do not redesign admin or invent a second shell.

**Starter mapping**
- reuse: Hallmark skill pack, design-with-hallmark orchestrator
- extend: `ui-surface-map.md` → React paths
- new: Hallmark-styled React marketing + tinted app chrome

## Implementation Steps

- [ ] Update `ui-surface-map.md` to `frontend/src/**` in-scope paths
- [ ] `/design-with-hallmark` with verb choice (default build)
- [ ] Apply tokens + marketing + shell tint only
- [ ] Mark this plan complete when visuals land

## Risks & Dependencies

- Depends on: spa-app-shell (routes/files exist to style)
- Avoid full dashboard IA redesign (skill rule)

## Expected Outcome

Marketing and app chrome look intentional (Hallmark gates), not Bootstrap defaults or generic AI purple gradients.

---
Owner: Jack Wilkins
Last reviewed: 2026-08-26
Review cadence: on change
