---
status: Pending Review
owner: Jack Wilkins
created: 2026-08-26
updated: 2026-08-26
---

# SPA + DRF foundation

## Context

The cookiecutter must become a simple React SPA + Django REST API starter. Product UIs today are Django templates; `frontend/` is only a CopilotKit Vite embed. Decision (2026-08-26): grow `frontend/` into the SPA; session auth; Vite proxy in dev.

## Findings

- `core/requirements.txt` has no `djangorestframework`.
- Templates under `core/templates/`; Copilot builds to `core/static/frontend/`.
- `frontend/vite.config.ts` outDir is Django static; entry is Copilot-only.

## Root Cause

There is no first-class JSON API or SPA shell—only server HTML plus an embedded widget.

## Proposed Solution

Add DRF with SessionAuthentication (+ CSRF), mount `/api/…`, configure Vite to proxy `/api`, `/accounts`, `/copilot` to Django, and change the Vite app into a multi-page SPA entry (router) while keeping a path to ship built assets via WhiteNoise in prod.

**Starter mapping**
- reuse: Django project, WhiteNoise, Docker, allauth sessions
- extend: `frontend/` Vite config + `core/core/urls.py` / settings
- new app: optional thin `core/api/` package or per-app `serializers`/`viewsets`

## Implementation Steps

- [ ] Add `djangorestframework` to `core/requirements.txt` and settings `INSTALLED_APPS`
- [ ] Configure DRF defaults: SessionAuthentication, IsAuthenticated where appropriate
- [ ] Mount `/api/` router in `core/core/urls.py`
- [ ] Vite: SPA entry + proxy `/api`, `/accounts`, `/copilot` → Django; adjust `base`/`outDir` for SPA deploy
- [ ] Dev scripts documented: Django + `vite` concurrently
- [ ] Prod: build SPA → static (or dist served by WhiteNoise / catch-all) (requires migration only if new models—none expected)

## Risks & Dependencies

- Catch-all SPA routing must not swallow `/admin/`, `/api/`, webhooks
- CSRF for session POSTs from SPA
- Depends on: auth SPA, shell plans

## Expected Outcome

Clone can run Django + Vite with `/api/` health or me endpoint and an empty React shell loading through the proxy.

---
Owner: Jack Wilkins
Last reviewed: 2026-08-26
Review cadence: on change
