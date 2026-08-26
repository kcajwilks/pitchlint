# CopilotKit + Agno (Django + React SPA)

In-app product chat wired to a Django AG-UI runtime and an Agno agent with workspace tools.

## What you get

- `CopilotSidebar` on authenticated app routes when Copilot is enabled (lazy-loaded)
- Django REST runtime at `/copilot/*` (SSE / AG-UI)
- Agno agent that can list/create/update projects and generate AI briefs
- Route context (`pathname`, `projectId`) injected into each run
- Thread persistence via `copilot` models

## Enable

In `core/.env`:

```env
COPILOT_ENABLED="1"
OPENAI_API_KEY="..."
AGNO_MODEL_ID="gpt-4o"
```

Restart Django after changing `.env`. Sign in, then open Dashboard or Workspace.

The SPA reads `copilot_enabled` from `/api/config/` (no Vite flag required). CopilotKit is not downloaded until that flag is true.

## Run

Use Vite for UI work (`cd frontend && npm run dev` → http://127.0.0.1:5173/), with Django on http://127.0.0.1:8000/.

## Runtime endpoints

- `GET /copilot/info` (also `GET`/`POST /copilot` for CopilotKit transport detect)
- `POST /copilot/agent/default/run` (SSE)
- `POST /copilot/agent/default/stop/<thread_id>`
- `POST /copilot/reset`

Auth: session cookie (`credentials="include"`) + `X-CSRFToken`. Unauthenticated calls return JSON `401` (not HTML).

## Files

- Backend: `core/copilot/ai.py`, `tools.py`, `views.py`, `auth.py`, `models.py`
- Frontend: `frontend/src/components/AppCopilot.tsx` (gate) + `CopilotHost.tsx` (CopilotKit UI)
- Agent skill (clones): [`.cursor/skills/copilotkit-agno/`](../.cursor/skills/copilotkit-agno/SKILL.md) (pack: [pack.md](../.cursor/skills/references/pack.md))
- Docs: [CopilotKit v2](https://docs.copilotkit.ai/reference/v2) · [Agno](https://docs.agno.com/)
