import os
from dataclasses import dataclass
from typing import Optional

from agno.agent import Agent
from agno.models.openai import OpenAIChat

from .tools import (
    create_project,
    generate_project_ai_brief,
    get_project,
    list_projects,
    update_project,
)


@dataclass(frozen=True)
class _AgentBundle:
    agent: Agent


_BUNDLE: Optional[_AgentBundle] = None

_INSTRUCTIONS = """You are the in-app product copilot for this SaaS (think Lovable / Cursor chat).
You help the signed-in user build and manage their Workspace by taking action, not by lecturing.

Style:
- Be concise and product-oriented.
- Prefer calling tools over telling the user which buttons to click.
- After mutations, say what changed and the project id.
- If context includes a current project id or route, use it unless the user asks about something else.
- Never invent project ids; list or look them up first when unsure.
- You cannot delete projects, change billing, or access other users' data.

Tools:
- list_projects, get_project, create_project, update_project, generate_project_ai_brief
"""


def get_copilot_agent() -> Agent:
    """Create once and reuse (do not construct inside request loops)."""
    global _BUNDLE
    if _BUNDLE is not None:
        return _BUNDLE.agent

    model_id = os.getenv("AGNO_MODEL_ID", "gpt-4o")
    agent = Agent(
        model=OpenAIChat(id=model_id),
        instructions=_INSTRUCTIONS,
        tools=[
            list_projects,
            get_project,
            create_project,
            update_project,
            generate_project_ai_brief,
        ],
        markdown=True,
    )
    _BUNDLE = _AgentBundle(agent=agent)
    return agent


def get_copilot_model_id() -> str:
    return os.getenv("AGNO_MODEL_ID", "gpt-4o")
