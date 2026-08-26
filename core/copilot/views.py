import json
import uuid
from typing import Any, Iterable

from django.conf import settings
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from agno.run.agent import RunContentEvent

from .ai import get_copilot_agent
from .auth import api_login_required
from .models import CopilotMessage, CopilotThread
from .tools import reset_copilot_user, set_copilot_user


def _copilot_enabled() -> bool:
    return bool(getattr(settings, "COPILOT_ENABLED", False))


def _sse(event: dict) -> str:
    return f"data: {json.dumps(event, separators=(',', ':'))}\n\n"


def _get_or_create_thread(*, user, thread_id: str) -> CopilotThread:
    thread, _ = CopilotThread.objects.get_or_create(owner=user, thread_id=thread_id)
    return thread


def _message_text(message: Any) -> str:
    if not isinstance(message, dict):
        return ""
    content = message.get("content")
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = []
        for part in content:
            if isinstance(part, dict) and part.get("type") == "text":
                parts.append(str(part.get("text") or ""))
            elif isinstance(part, str):
                parts.append(part)
        return "".join(parts).strip()
    return str(content or "").strip()


def _format_context(body: dict) -> str:
    chunks: list[str] = []
    context = body.get("context")
    if isinstance(context, list) and context:
        lines = []
        for item in context:
            if not isinstance(item, dict):
                continue
            desc = item.get("description") or item.get("descriptionText") or "context"
            value = item.get("value")
            if value is None:
                value = item.get("content")
            lines.append(f"- {desc}: {value}")
        if lines:
            chunks.append("UI context:\n" + "\n".join(lines))
    props = body.get("forwardedProps") or body.get("properties") or {}
    if isinstance(props, dict) and props:
        chunks.append("Client properties:\n" + json.dumps(props, ensure_ascii=False))
    state = body.get("state")
    if isinstance(state, dict) and state:
        chunks.append("Agent state:\n" + json.dumps(state, ensure_ascii=False))
    return "\n\n".join(chunks)


def _build_prompt(body: dict, last_user_text: str) -> str:
    context_block = _format_context(body)
    messages = body.get("messages") or []
    history: list[str] = []
    if isinstance(messages, list):
        for msg in messages[-16:]:
            if not isinstance(msg, dict):
                continue
            role = str(msg.get("role") or "")
            if role not in {"user", "assistant", "system"}:
                continue
            text = _message_text(msg)
            if not text:
                continue
            history.append(f"{role}: {text}")
    parts = []
    if context_block:
        parts.append(context_block)
    if history:
        parts.append("Conversation so far:\n" + "\n".join(history))
    parts.append(f"Respond to the latest user message:\n{last_user_text or 'Say hello.'}")
    return "\n\n".join(parts)


def _public_error_message(exc: BaseException) -> str:
    raw = str(exc)
    lowered = raw.lower()
    if "api key" in lowered or "invalid_api_key" in lowered:
        return "OpenAI API key is missing or invalid. Set OPENAI_API_KEY in core/.env and restart Django."
    if "rate limit" in lowered:
        return "The model provider rate-limited this request. Try again shortly."
    # Avoid leaking provider payloads / secrets into the browser.
    if len(raw) > 280:
        return raw[:277] + "..."
    return raw or "Copilot run failed."


def _chunk_text(text: str, size: int = 48) -> Iterable[str]:
    if not text:
        return
    for i in range(0, len(text), size):
        yield text[i : i + size]


def _info_payload():
    if not _copilot_enabled():
        return JsonResponse({"agents": {}}, status=200)
    return JsonResponse(
        {
            "version": "django-copilot-0.2",
            "mode": "sse",
            "agents": {
                "default": {
                    "description": "In-app product copilot (Agno + workspace tools)",
                    "capabilities": {},
                }
            },
        }
    )


@require_GET
@api_login_required
def info(request):
    return _info_payload()


@require_http_methods(["GET", "POST"])
@api_login_required
def runtime(request):
    """CopilotKit hits /copilot (no slash) during transport auto-detect."""
    if request.method == "GET":
        return _info_payload()
    try:
        body = json.loads(request.body.decode("utf-8") or "{}")
    except Exception:
        body = {}
    if body.get("method") == "info":
        return _info_payload()
    return JsonResponse({"error": "Unknown CopilotKit method."}, status=400)


@require_POST
@api_login_required
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

    thread = _get_or_create_thread(user=request.user, thread_id=thread_id)
    last_user_text = ""
    if isinstance(messages, list) and messages:
        for msg in reversed(messages):
            if isinstance(msg, dict) and msg.get("role") == "user":
                last_user_text = _message_text(msg)
                if last_user_text:
                    break
    if last_user_text:
        CopilotMessage.objects.create(thread=thread, role=CopilotMessage.Role.USER, content=last_user_text)

    prompt = _build_prompt(body, last_user_text)
    agent = get_copilot_agent()
    user = request.user

    def gen() -> Iterable[str]:
        yield _sse({"type": "RUN_STARTED", "threadId": thread_id, "runId": run_id})
        message_id = str(uuid.uuid4())
        yield _sse({"type": "TEXT_MESSAGE_START", "messageId": message_id, "role": "assistant"})

        token = set_copilot_user(user)
        assembled = ""
        try:
            for event in agent.run(prompt, stream=True, stream_events=True):
                if not isinstance(event, RunContentEvent):
                    continue
                content = event.content
                if not isinstance(content, str) or not content:
                    continue
                assembled += content
                yield _sse({"type": "TEXT_MESSAGE_CONTENT", "messageId": message_id, "delta": content})
            if not assembled:
                result = agent.run(prompt)
                text = getattr(result, "content", None)
                assembled = text if isinstance(text, str) else str(text or "")
                err = getattr(result, "error", None) or getattr(result, "status", None)
                if err and str(err).lower() in {"error", "failed"} and not assembled:
                    raise RuntimeError(str(getattr(result, "messages", None) or err))
                if assembled.lower().startswith("incorrect api key") or "invalid_api_key" in assembled.lower():
                    raise RuntimeError(assembled)
                for chunk in _chunk_text(assembled):
                    yield _sse({"type": "TEXT_MESSAGE_CONTENT", "messageId": message_id, "delta": chunk})
        except Exception as exc:
            message = _public_error_message(exc)
            yield _sse({"type": "TEXT_MESSAGE_CONTENT", "messageId": message_id, "delta": message})
            yield _sse({"type": "TEXT_MESSAGE_END", "messageId": message_id})
            yield _sse(
                {
                    "type": "RUN_ERROR",
                    "message": message,
                    "threadId": thread_id,
                    "runId": run_id,
                }
            )
            return
        finally:
            reset_copilot_user(token)

        yield _sse({"type": "TEXT_MESSAGE_END", "messageId": message_id})
        yield _sse({"type": "RUN_FINISHED", "threadId": thread_id, "runId": run_id})
        if assembled:
            CopilotMessage.objects.create(
                thread=thread,
                role=CopilotMessage.Role.ASSISTANT,
                content=assembled,
            )

    resp = StreamingHttpResponse(gen(), content_type="text/event-stream")
    resp["Cache-Control"] = "no-cache"
    resp["X-Accel-Buffering"] = "no"
    return resp


@require_POST
@api_login_required
def agent_stop(request, agent_id: str, thread_id: str):
    if agent_id != "default":
        return JsonResponse({"ok": True})
    return JsonResponse({"ok": True})


@require_POST
@api_login_required
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
