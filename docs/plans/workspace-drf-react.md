---
status: Pending Review
owner: Jack Wilkins
created: 2026-08-26
updated: 2026-08-26
---

# Workspace Project as DRF + React sample

## Context

Keep `workspace.Project` as the end-to-end sample (CRUD + AI brief) proving API + SPA + Agno.

## Findings

- Models: `Project`, `ProjectBriefRun` in `core/workspace/`.
- Template CRUD + generate-brief view exist today.

## Root Cause

Sample domain is template-bound; no serializers/viewsets or React pages.

## Proposed Solution

DRF viewsets for projects (owner-scoped); endpoint to generate AI brief (reuse `workspace/ai.py`); React list/detail/create/edit pages calling `/api/…`.

**Starter mapping**
- reuse: models, `workspace/ai.py`, permissions patterns
- extend: workspace app with DRF
- new: React workspace pages

## Implementation Steps

- [ ] Serializers + ViewSets + router registration `(requires migration)` only if schema changes—prefer none
- [ ] Generate-brief API action
- [ ] React pages wired to API
- [ ] Remove template workspace views from primary UX

## Risks & Dependencies

- Depends on: spa-drf-foundation, spa-auth-allauth, spa-app-shell
- AI needs `OPENAI_API_KEY`

## Expected Outcome

Logged-in user can manage Projects and generate an AI brief entirely via React + `/api/`.

---
Owner: Jack Wilkins
Last reviewed: 2026-08-26
Review cadence: on change
