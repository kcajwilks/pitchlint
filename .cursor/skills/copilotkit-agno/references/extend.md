# Extend CopilotKit + Agno

Pack: [../../references/pack.md](../../references/pack.md). Stack is Django + this SPA. Extend `core/copilot/` and `frontend/src/components/` only.

Docs: [CopilotKit v2](https://docs.copilotkit.ai/reference/v2) · [Agno tools](https://docs.agno.com/agents/tools) · [Agno structured output](https://docs.agno.com/input-output/structured-output/agent)

## Agno: reuse + tools

```python
# WRONG — inside a view/loop
agent = Agent(model=OpenAIChat(id="gpt-4o"), tools=[...])

# RIGHT — module singleton (see core/copilot/ai.py)
def get_copilot_agent() -> Agent:
    ...
```

Python tools ([Agno](https://docs.agno.com/agents/tools)): specific name, docstring (when to call), type hints. Return short strings or JSON-serializable dicts. Scope rows with the signed-in user (`_user()` in `tools.py`), never “the first project”.

Do not use Team/Workflow unless a single agent + tools cannot do the job.

## Agno: structured job

```python
from pydantic import BaseModel, Field
from agno.agent import Agent
from agno.models.openai import OpenAIChat

class ProjectBrief(BaseModel):
    summary: str = Field(..., description="1-3 sentence summary")
    suggested_features: list[str]
    risks: list[str]

agent = Agent(
    model=OpenAIChat(id=os.getenv("AGNO_MODEL_ID", "gpt-4o")),
    instructions="...",
    output_schema=ProjectBrief,
    markdown=False,
)
brief: ProjectBrief = agent.run(prompt).content
```

Chat agents stay `markdown=True` without `output_schema`. Jobs that feed the UI use `output_schema`.

## CopilotKit v2: provider + sidebar

```tsx
import {
  CopilotKitProvider,
  CopilotSidebar,
  useAgentContext,
  useFrontendTool,
} from "@copilotkit/react-core/v2";
```

- `runtimeUrl="/copilot"`, `credentials="include"`, `useSingleEndpoint={false}`
- `headers={() => ({ "X-CSRFToken": getCookie("csrftoken") || "" })}`
- `CopilotSidebar` `agentId="default"` ([sidebar props](https://docs.copilotkit.ai/reference/v2/components/CopilotSidebar))

## CopilotKit v2: frontend tool

[`useFrontendTool`](https://docs.copilotkit.ai/reference/v2/hooks/useFrontendTool) — Zod params, handler in the browser. Persist through `/api/` + `frontend/src/api/client.ts`, not a new auth stack.

```tsx
useFrontendTool(
  {
    name: "focusProject",
    description: "Select a workspace project in the UI by id",
    parameters: z.object({
      projectId: z.number().describe("Project id"),
    }),
    handler: async ({ projectId }) => {
      navigate(`/workspace/${projectId}`);
      return `Opened project ${projectId}`;
    },
  },
  [],
);
```

Register under `CopilotKitProvider`. Prefer Agno tools for mutations that must be trusted server-side.

## CopilotKit v2: context

```tsx
useAgentContext({
  description: "Current app route and selection",
  value: { pathname, projectId },
});
```

Keep payloads tiny. The Django runtime already concatenates CopilotKit `context` into the Agno prompt (`views._format_context`).

## SSE errors

If the model fails, yield `TEXT_MESSAGE_CONTENT` with a public message, then `TEXT_MESSAGE_END` and `RUN_ERROR`. `RUN_ERROR` alone often leaves the sidebar blank.
