---
name: copilotkit-agno
description: >
  Extend CopilotKit v2 chat and Agno agents on this Django SaaS starter
  (SPA sidebar, Django AG-UI runtime, workspace tools, structured briefs).
  Use when adding Copilot tools or context, changing the Agno agent,
  wiring output_schema jobs, debugging /copilot SSE, or when the user
  mentions CopilotKit, Agno, AG-UI, CopilotSidebar, or in-app copilot.
---

# CopilotKit + Agno (this starter)

**Stack:** Django runtime + CopilotKit in the existing Vite React SPA. Never FastAPI, `@copilotkit/runtime` in `frontend/`, or a second app.

Pack: [`.cursor/skills/references/pack.md`](../references/pack.md). Inventory: [`django-saas-starter`](../django-saas-starter/SKILL.md). Chat UI is **CopilotKit v2**. Agents, tools, and typed jobs are **Agno**.

Upstream: [CopilotKit v2](https://docs.copilotkit.ai/reference/v2) · [Agno](https://docs.agno.com/)

New product AI: plan first (`/plan-saas-from-starter` + `docs-plans`). Do not Hallmark the copilot chrome ([ui-surface-map](../references/ui-surface-map.md)).

## Split

| Need | Use |
|------|-----|
| Sidebar / chat / client tools / route context | CopilotKit in `frontend/src/components/` |
| Model calls, Python tools, streaming | Agno in `core/copilot/` |
| Typed JSON for a button/API (briefs, extracts) | Separate Agno agent + `output_schema` (see `core/workspace/ai.py`) |

## This repo

Lazy gate `AppCopilot` → `CopilotHost` (`CopilotKitProvider` + `CopilotSidebar`, `runtimeUrl="/copilot"`, `credentials="include"`, CSRF header, `useSingleEndpoint={false}`). Django `GET /copilot/info` and `POST /copilot/agent/default/run` (SSE) run `get_copilot_agent()`. Tools use a request `ContextVar` for the signed-in user.

Enable: `COPILOT_ENABLED=1` + valid `OPENAI_API_KEY` in `core/.env`, restart Django, sign in, open Dashboard/Workspace on Vite `:5173`.

Paths, env, pitfalls: [references/starter.md](references/starter.md).

## Rules

1. **Reuse** Agno `Agent` instances (`get_copilot_agent` / `get_project_brief_agent`). Never construct inside a request loop.
2. **Chat tools** = Python functions with name + docstring + type hints on `Agent(tools=[...])`. Bind the Django user the way `core/copilot/tools.py` does.
3. **Structured jobs** = `output_schema=PydanticModel`; read `result.content`. Do not parse free-form chat for CRUD payloads.
4. **SPA only**: extend `CopilotHost` / `AppCopilot`. No Django product templates, no extra Vite app.
5. Import CopilotKit from `@copilotkit/react-core/v2`. Put `agentId` on `CopilotSidebar`, not a second runtime.
6. Runtime responses must be **JSON or SSE**, never `index.html`. Keep `/copilot` out of the SPA catch-all.

## Workflows

**Backend tool (usual):** add a function in `core/copilot/tools.py` → register on the agent in `ai.py` → mention it in `_INSTRUCTIONS` → scope by `_user()`.

**Client tool:** `useFrontendTool` + Zod in a component under `CopilotKitProvider`. Use for UI-only actions; persist via `/api/` with the existing session client.

**Context:** `useAgentContext` for route/selection (already: `pathname`, `projectId`). Keep values small.

**Structured job:** new or existing Agno helper next to the domain app (pattern: `workspace/ai.py`), expose via DRF, not via chat-only parsing.

How-to snippets: [references/extend.md](references/extend.md).

## Verify

- Vite `:5173` + Django `:8000`; `/copilot/info` is JSON 200 when signed in.
- Invalid OpenAI keys fail in the sidebar (and Django logs), not as a silent hang.
- `COPILOT_ENABLED=0` must not load CopilotKit (lazy gate in `AppCopilot`).

## Related

[pack.md](../references/pack.md) · [`django-saas-starter`](../django-saas-starter/SKILL.md) · [`plan-saas-from-starter`](../plan-saas-from-starter/SKILL.md) · [`docs-plans`](../docs-plans/SKILL.md) · [ui-surface-map.md](../references/ui-surface-map.md) (Copilot out of Hallmark scope)
