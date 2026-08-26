---
status: Pending Review
owner: Jack Wilkins
created: 2026-08-26
updated: 2026-08-26
---

# SPA auth (allauth + session)

## Context

Full React cutover needs login/signup/logout/Google without server-rendered allauth templates. Decision: session cookies + allauth, same-origin via Vite proxy.

## Findings

- allauth at `/accounts/`; templates under `core/templates/account/` and `allauth/`.
- Settings IA under `/settings/*` is template-based.

## Root Cause

Auth UX is HTML-only; SPA has no first-class session login flow.

## Proposed Solution

Expose session-friendly auth for the SPA: CSRF cookie endpoint, login/logout/signup (and current user) via DRF or thin JSON views wrapping allauth; React pages for login/signup; keep Google OAuth via allauth redirects returning to the SPA. Preserve django.contrib.admin login separately.

**Starter mapping**
- reuse: allauth, Google SocialApp, sessions
- extend: accounts flow + React routes
- new: React auth pages; optional `api/auth` views

## Implementation Steps

- [ ] `GET` CSRF / `GET /api/me/` (or equivalent)
- [ ] Login / logout / signup JSON or form-compatible endpoints usable from SPA
- [ ] React routes: `/login`, `/signup`; redirect unauthenticated users
- [ ] Google OAuth: redirect round-trip back into SPA
- [ ] Remove dependency on account HTML templates for primary UX

## Risks & Dependencies

- OAuth redirect URIs and SITE_ID
- CSRF header on mutating requests
- Depends on: spa-drf-foundation

## Expected Outcome

User can register/login/logout from React with session cookie; `/api/me/` returns the user.

---
Owner: Jack Wilkins
Last reviewed: 2026-08-26
Review cadence: on change
