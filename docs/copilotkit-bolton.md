# CopilotKit + Agno (bolt-on, standard)

This repo includes a “standard” CopilotKit + Agno setup (per CopilotKit’s Agno quickstart) alongside the Django app.

- Docs reference: [Agno quickstart (bring your own)](https://docs.copilotkit.ai/agno/quickstart?agent=bring-your-own)

## What runs where

- **Agno agent server** (`agent/`): exposes an AG-UI endpoint at `http://127.0.0.1:8000/agui`
- **CopilotKit UI + Runtime** (`ui/`): Next.js app at `http://127.0.0.1:3000` with runtime endpoint `/api/copilotkit`
- **Django app** (`core/`): unchanged for now

## 1) Configure environment

Set your key for the agent:

```bash
export OPENAI_API_KEY="..."
```

## 2) Start the agent

```bash
cd agent
uv run main.py
```

Agent endpoint: `http://127.0.0.1:8000/agui`

## 3) Start the UI

```bash
cd ui
npm run dev
```

Open: `http://127.0.0.1:3000`

## Troubleshooting

- If the UI loads but chat fails, confirm the agent is reachable at `http://127.0.0.1:8000/agui`.
- If you’re running the agent on a different host/port, update `ui/src/app/api/copilotkit/route.ts`.

