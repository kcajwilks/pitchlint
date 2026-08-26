# Starter map (CopilotKit + Agno)

Pack: [../../references/pack.md](../../references/pack.md). Human setup: [`docs/copilotkit.md`](../../../docs/copilotkit.md). Capability map: [`django-saas-starter`](../../django-saas-starter/SKILL.md). Plan new AI work first (`docs-plans`); do not Hallmark this chrome.

## Files

| Role | Path |
|------|------|
| Lazy gate | `frontend/src/components/AppCopilot.tsx` |
| Provider + sidebar | `frontend/src/components/CopilotHost.tsx` |
| Mount | `frontend/src/layouts/Layouts.tsx` (`AppLayout` only) |
| Flag | `GET /api/config/` → `copilot_enabled` (`core/api/config.py`) |
| Chat agent | `core/copilot/ai.py` |
| Tools + user bind | `core/copilot/tools.py` |
| AG-UI SSE | `core/copilot/views.py` |
| URLs | `core/copilot/urls.py` + `path("copilot", …)` in `core/core/urls.py` |
| Threads | `core/copilot/models.py` |
| Structured brief | `core/workspace/ai.py` (`output_schema=ProjectBrief`) |
| Brief API | `POST /api/projects/<id>/generate-brief/` |

## Runtime (REST, not single-endpoint)

CopilotKit v2 auto-detect will POST `/copilot` if `GET /copilot/info` is not 2xx. This starter forces `useSingleEndpoint={false}` and serves JSON at `/copilot` so the SPA shell is never parsed as JSON.

| Method | Path |
|--------|------|
| GET | `/copilot/info` |
| GET/POST | `/copilot` (info / `{method: "info"}`) |
| POST | `/copilot/agent/default/run` (SSE) |
| POST | `/copilot/agent/default/stop/<thread_id>` |
| POST | `/copilot/reset` |

Auth: session cookie + `X-CSRFToken`. Unauthenticated → JSON 401. CSRF failures on `/copilot` and `/api/` → JSON 403 (`core/core/csrf.py`).

SSE event types the runtime emits: `RUN_STARTED`, `TEXT_MESSAGE_*`, `RUN_ERROR`, `RUN_FINISHED`.

## Env

```env
OPENAI_API_KEY="sk-..."
AGNO_MODEL_ID="gpt-4o"
COPILOT_ENABLED="1"
```

Restart Django after `.env` changes (`load_dotenv` runs at settings import).

## Pitfalls

- **Invalid API key** → OpenAI 401; chat looks idle unless `RUN_ERROR` is also sent as `TEXT_MESSAGE_CONTENT` (see `views.agent_run`).
- **Dev UI** is Vite `http://127.0.0.1:5173/` (proxies `/copilot` and `/api`). Django `:8000` serves a frozen `npm run build` unless you rebuild.
- **Do not git** `core/static/spa/` (Vite outDir). Do not commit a second Copilot Vite/Next app.
- Styles in this starter: `@copilotkit/react-ui/v2/styles.css`. Upstream v2 examples often use `@copilotkit/react-core/v2/styles.css` — do not import both without checking overlap.
- Provider: this starter uses `CopilotKitProvider`. v2 docs also show `<CopilotKit>` from `@copilotkit/react-core/v2` ([component ref](https://docs.copilotkit.ai/reference/v2/components/CopilotKit)). Keep one provider tree.
