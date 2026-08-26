---
status: Pending Review
owner: Jack Wilkins
created: 2026-08-26
updated: 2026-08-26
---

# CopilotKit inside the React SPA

## Context

Copilot today is embedded via Django template partial + static `copilot.js`. SPA cutover should host CopilotKit as normal React components in `frontend/`.

## Findings

- `frontend/src/copilot.tsx` embed entry; `core/templates/_partials/_copilot.html`.
- Runtime at `/copilot/`.

## Root Cause

Copilot is a bolted-on static bundle, not part of the SPA tree.

## Proposed Solution

Integrate CopilotKit providers/UI into the SPA (workspace/detail or layout); Vite proxy `/copilot`; retire template partial and separate embed-only build shape if superseded by SPA build.

**Starter mapping**
- reuse: `core/copilot/` runtime, Agno agent, models
- extend: `frontend/src` Copilot usage
- new: none on backend if runtime stays

## Implementation Steps

- [ ] Mount CopilotKit in SPA where product needs it (e.g. project detail)
- [ ] Proxy `/copilot` in Vite; env `COPILOT_ENABLED`
- [ ] Remove `_copilot.html` from primary flow
- [ ] Ensure production SPA build still includes Copilot assets

## Risks & Dependencies

- Depends on: spa-app-shell, workspace-drf-react (if chat is on project page)

## Expected Outcome

Copilot chat works inside the React app without Django template includes.

---
Owner: Jack Wilkins
Last reviewed: 2026-08-26
Review cadence: on change
