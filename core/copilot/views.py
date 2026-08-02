import json
import uuid
from typing import Iterable

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, StreamingHttpResponse
from django.views.generic import TemplateView
from django.views.decorators.http import require_GET, require_POST

from .ai import get_copilot_agent
from .models import CopilotMessage, CopilotThread


def _copilot_enabled() -> bool:
    return bool(getattr(settings, "COPILOT_ENABLED", False))


def _sse(event: dict) -> str:
    return f"data: {json.dumps(event, separators=(',', ':'))}\n\n"


def _get_or_create_thread(*, user, thread_id: str) -> CopilotThread:
    thread, _ = CopilotThread.objects.get_or_create(owner=user, thread_id=thread_id)
    return thread


@require_GET
@login_required
def info(request):
    if not _copilot_enabled():
        return JsonResponse({"agents": {}}, status=200)
    return JsonResponse(
        {
            "version": "django-copilot-0.1",
            "mode": "sse",
            "agents": {
                "default": {
                    "description": "Django Copilot (Agno)",
                    "capabilities": {},
                }
            },
        }
    )


@require_POST
@login_required
def agent_run(request, agent_id: str):
    if not _copilot_enabled():
        return JsonResponse({"error": "Copilot is disabled."}, status=404)
    if agent_id != "default":
        return JsonResponse({"error": "Unknown agent."}, status=404)

    try:
        body = json.loads(request.body.decode("utf-8") or "{}")
    except Exception:
        body = {}

    thread_id = str(body.get("threadId") or body.get("thread_id") or "").strip() or f"thread_{request.user.id}"
    run_id = str(body.get("runId") or body.get("run_id") or uuid.uuid4()).strip()
    messages = body.get("messages") or []

    # Persist incoming user message (best-effort).
    thread = _get_or_create_thread(user=request.user, thread_id=thread_id)
    last_user_text = ""
    if isinstance(messages, list) and messages:
        last = messages[-1]
        if isinstance(last, dict) and last.get("role") == "user":
            last_user_text = str(last.get("content") or "").strip()
    if last_user_text:
        CopilotMessage.objects.create(thread=thread, role=CopilotMessage.Role.USER, content=last_user_text)

    agent = get_copilot_agent()
    prompt = last_user_text or "Say hello."

    def gen() -> Iterable[str]:
        # AG-UI protocol event types (see @ag-ui/core EventType).
        yield _sse({"type": "RUN_STARTED", "threadId": thread_id, "runId": run_id})
        message_id = str(uuid.uuid4())
        yield _sse({"type": "TEXT_MESSAGE_START", "messageId": message_id, "role": "assistant"})
        try:
            result = agent.run(prompt).content
            text = getattr(result, "message", None) or (result if isinstance(result, str) else str(result))
        except Exception as exc:
            yield _sse({"type": "RUN_ERROR", "message": str(exc), "threadId": thread_id, "runId": run_id})
            return
        yield _sse({"type": "TEXT_MESSAGE_CONTENT", "messageId": message_id, "delta": text})
        yield _sse({"type": "TEXT_MESSAGE_END", "messageId": message_id})
        yield _sse({"type": "RUN_FINISHED", "threadId": thread_id, "runId": run_id})

        CopilotMessage.objects.create(thread=thread, role=CopilotMessage.Role.ASSISTANT, content=text)

    resp = StreamingHttpResponse(gen(), content_type="text/event-stream")
    resp["Cache-Control"] = "no-cache"
    return resp


@require_POST
@login_required
def agent_stop(request, agent_id: str, thread_id: str):
    # Minimal stop endpoint; real implementations would abort in-flight runs.
    if agent_id != "default":
        return JsonResponse({"ok": True})
    return JsonResponse({"ok": True})


@require_POST
@login_required
def reset(request):
    if not _copilot_enabled():
        return JsonResponse({"error": "Copilot is disabled."}, status=404)
    try:
        body = json.loads(request.body.decode("utf-8") or "{}")
    except Exception:
        body = {}
    thread_id = str(body.get("threadId") or body.get("thread_id") or "").strip()
    if not thread_id:
        return JsonResponse({"error": "Missing threadId."}, status=400)
    CopilotThread.objects.filter(owner=request.user, thread_id=thread_id).delete()
    return JsonResponse({"ok": True})


class CopilotDemoInlineView(TemplateView):
    template_name = "copilot/demo_inline.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["active_nav"] = "copilot"
        ctx["app_page_title"] = "Copilot · Inline"
        return ctx


class CopilotDemoSidebarView(TemplateView):
    template_name = "copilot/demo_sidebar.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["active_nav"] = "copilot"
        ctx["app_page_title"] = "Copilot · Sidebar"
        return ctx


class CopilotDemoPopupView(TemplateView):
    template_name = "copilot/demo_popup.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["active_nav"] = "copilot"
        ctx["app_page_title"] = "Copilot · Popup"
        return ctx

