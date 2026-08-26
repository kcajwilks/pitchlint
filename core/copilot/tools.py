"""Workspace tools for the in-app Copilot (bound to the current request user)."""

from __future__ import annotations

from contextvars import ContextVar
from typing import Optional

from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone

from workspace.ai import generate_project_brief, get_project_brief_model_id
from workspace.models import Project, ProjectBriefRun

_current_user: ContextVar[Optional[AbstractBaseUser]] = ContextVar("copilot_user", default=None)


def set_copilot_user(user: AbstractBaseUser) -> object:
    return _current_user.set(user)


def reset_copilot_user(token: object) -> None:
    _current_user.reset(token)


def _user() -> AbstractBaseUser:
    user = _current_user.get()
    if user is None or not getattr(user, "is_authenticated", False):
        raise RuntimeError("Copilot tools require an authenticated user.")
    return user


def list_projects() -> str:
    """List the current user's workspace projects (id, name, description)."""
    qs = Project.objects.filter(owner=_user()).order_by("-updated_at")[:25]
    if not qs:
        return "No projects yet."
    lines = []
    for p in qs:
        desc = (p.description or "").strip().replace("\n", " ")
        if len(desc) > 120:
            desc = desc[:117] + "..."
        lines.append(f"- #{p.id}: {p.name}" + (f" — {desc}" if desc else ""))
    return "\n".join(lines)


def get_project(project_id: int) -> str:
    """Get details for one of the current user's projects, including AI brief if present."""
    try:
        p = Project.objects.get(pk=project_id, owner=_user())
    except Project.DoesNotExist:
        return f"Project #{project_id} not found (or not yours)."
    brief = (p.ai_brief or "").strip()
    brief_note = brief[:2000] if brief else "(none)"
    return (
        f"id: {p.id}\n"
        f"name: {p.name}\n"
        f"description: {p.description or ''}\n"
        f"ai_brief_updated_at: {p.ai_brief_updated_at or 'never'}\n"
        f"ai_brief:\n{brief_note}"
    )


def create_project(name: str, description: str = "") -> str:
    """Create a workspace project owned by the current user."""
    name = (name or "").strip()
    if not name:
        return "Error: name is required."
    p = Project.objects.create(
        owner=_user(),
        name=name[:200],
        description=(description or "").strip(),
    )
    return f"Created project #{p.id}: {p.name}"


def update_project(
    project_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
) -> str:
    """Update name and/or description on one of the current user's projects."""
    try:
        p = Project.objects.get(pk=project_id, owner=_user())
    except Project.DoesNotExist:
        return f"Project #{project_id} not found (or not yours)."
    fields = ["updated_at"]
    if name is not None:
        cleaned = name.strip()
        if not cleaned:
            return "Error: name cannot be empty."
        p.name = cleaned[:200]
        fields.append("name")
    if description is not None:
        p.description = description
        fields.append("description")
    if len(fields) == 1:
        return "Nothing to update (pass name and/or description)."
    p.save(update_fields=fields)
    return f"Updated project #{p.id}: {p.name}"


def generate_project_ai_brief(project_id: int) -> str:
    """Generate (or regenerate) the AI brief for a project the user owns."""
    try:
        p = Project.objects.get(pk=project_id, owner=_user())
    except Project.DoesNotExist:
        return f"Project #{project_id} not found (or not yours)."
    model_id = get_project_brief_model_id()
    try:
        brief = generate_project_brief(p)
    except Exception as exc:
        ProjectBriefRun.objects.create(
            project=p,
            status=ProjectBriefRun.Status.ERROR,
            model_id=model_id,
            error_message=str(exc),
        )
        return f"Brief generation failed: {exc}"
    brief_json = brief.model_dump_json(indent=2)
    ProjectBriefRun.objects.create(
        project=p,
        status=ProjectBriefRun.Status.SUCCESS,
        model_id=model_id,
        brief_json=brief_json,
    )
    p.ai_brief = brief_json
    p.ai_brief_updated_at = timezone.now()
    p.save(update_fields=["ai_brief", "ai_brief_updated_at", "updated_at"])
    return f"Generated AI brief for project #{p.id}. Preview:\n{brief_json[:1500]}"
