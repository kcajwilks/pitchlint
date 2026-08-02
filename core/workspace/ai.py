import os
from dataclasses import dataclass
from typing import Optional

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from pydantic import BaseModel, Field

from .models import Project


class ProjectBrief(BaseModel):
    summary: str = Field(..., description="1-3 sentence plain-English summary")
    suggested_features: list[str] = Field(..., description="Concrete next features to build")
    risks: list[str] = Field(..., description="Key implementation risks or pitfalls")


@dataclass(frozen=True)
class _AgentBundle:
    agent: Agent


_BUNDLE: Optional[_AgentBundle] = None


def get_project_brief_agent() -> Agent:
    global _BUNDLE
    if _BUNDLE is not None:
        return _BUNDLE.agent

    model_id = os.getenv("AGNO_MODEL_ID", "gpt-4o")
    agent = Agent(
        model=OpenAIChat(id=model_id),
        instructions=(
            "You help build a Django SaaS app. "
            "Given a project name/description, produce a short project brief with actionable next steps. "
            "Be concrete and avoid generic advice."
        ),
        output_schema=ProjectBrief,
        markdown=False,
    )
    _BUNDLE = _AgentBundle(agent=agent)
    return agent


def get_project_brief_model_id() -> str:
    return os.getenv("AGNO_MODEL_ID", "gpt-4o")


def generate_project_brief(project: Project) -> ProjectBrief:
    agent = get_project_brief_agent()
    prompt = "\n".join(
        [
            "Generate a project brief for this Workspace project.",
            f"Name: {project.name}",
            f"Description: {project.description or '(none)'}",
        ]
    )
    result = agent.run(prompt).content
    if isinstance(result, ProjectBrief):
        return result
    return ProjectBrief.model_validate(result)
