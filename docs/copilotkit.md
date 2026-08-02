# CopilotKit + Agno (Django integration)

This starter can embed a CopilotKit React UI inside Django templates and connect it to an Agno-powered agent via a Django “runtime” endpoint.

## What you get

- A React chat UI embedded on the Workspace project page
- A Django runtime at `/copilot/*` that CopilotKit can talk to
- Agno agent implementation in `core/copilot/ai.py`
- Optional persistence in Django DB via `copilot` models

## Prerequisites

- Node.js 20+
- Python 3.9+
- `OPENAI_API_KEY` set

## Enable Copilot

In `core/.env`:

```env
COPILOT_ENABLED="1"
OPENAI_API_KEY="..."
AGNO_MODEL_ID="gpt-4o"
```

## Install frontend dependencies

From the repo root:

```bash
cd frontend
npm install
```

## Build the embedded frontend bundle

This starter builds the Copilot UI into Django static assets:

- output: `core/static/frontend/`
- entry: `core/static/frontend/copilot.js`

Build once:

```bash
cd frontend
npm run build
```

Watch mode (rebuild on changes):

```bash
cd frontend
npm run dev
```

## Docker

Docker Compose loads `core/.env` and builds the frontend bundle during the image build (see `Dockerfile`).

```bash
docker compose up --build
```

Ensure `core/.env` includes:

```env
COPILOT_ENABLED="1"
OPENAI_API_KEY="..."
```


From the repo root:

```bash
cd core
python manage.py migrate
python manage.py runserver
```

Then open a Workspace project and use the embedded Copilot panel.

## Runtime endpoints

CopilotKit discovers and runs the agent via:

- `GET /copilot/info`
- `POST /copilot/agent/default/run` (SSE / AG-UI events)

The integration uses cookie auth (`credentials="include"`) and sends `X-CSRFToken` from the browser’s `csrftoken` cookie.

## Files to know

- Backend:
  - `core/copilot/ai.py`
  - `core/copilot/views.py`
  - `core/copilot/models.py`
  - `core/copilot/urls.py`
- Frontend:
  - `frontend/src/copilot.tsx`
  - `frontend/vite.config.ts`
- Template partial:
  - `core/templates/_partials/_copilot.html`

