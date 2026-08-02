import os
from dataclasses import dataclass
from typing import Any, Optional

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from pydantic import BaseModel, Field


class ProposedAction(BaseModel):
    action: str = Field(..., description="Action name (create_project, update_project_name, update_project_description)")
    summary: str = Field(..., description="One-line description of what will change")
    params: dict[str, Any] = Field(default_factory=dict, description="Action parameters")


class CopilotReply(BaseModel):
    message: str = Field(..., description="Assistant response to show the user")
    proposed_actions: list[ProposedAction] = Field(
        default_factory=list,
        description="Actions to propose for user confirmation. Do not assume execution.",
    )


@dataclass(frozen=True)
class _AgentBundle:
    agent: Agent


_BUNDLE: Optional[_AgentBundle] = None


def get_copilot_agent() -> Agent:
    global _BUNDLE
    if _BUNDLE is not None:
        return _BUNDLE.agent

    model_id = os.getenv("AGNO_MODEL_ID", "gpt-4o")
    agent = Agent(
        model=OpenAIChat(id=model_id),
        instructions=(
            "You are a product copilot inside a Django SaaS app.\n"
            "You help the user manage a Workspace project.\n\n"
            "Rules:\n"
            "- You may propose actions, but never claim you executed them.\n"
            "- Only propose these actions: create_project, update_project_name, update_project_description.\n"
            "- Keep proposed action params minimal and explicit.\n"
            "- If the user asks to delete or do anything outside the allowed actions, explain it's not supported.\n"
        ),
        output_schema=CopilotReply,
        markdown=False,
    )
    _BUNDLE = _AgentBundle(agent=agent)
    return agent


def get_copilot_model_id() -> str:
    return os.getenv("AGNO_MODEL_ID", "gpt-4o")

