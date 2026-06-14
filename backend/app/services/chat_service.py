"""Chat streaming service wrapping the GenAI copilot, with persistence."""
from __future__ import annotations

import json
import uuid
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import SessionLocal
from app.integrations.genai import copilot_chat, format_response
from app.models.chat_log import ChatMessage
from app.schemas.chat import ChatRequest


def _sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


def _coerce_session(value: str) -> uuid.UUID:
    try:
        return uuid.UUID(value)
    except (ValueError, TypeError):
        return uuid.uuid4()


async def stream_chat(req: ChatRequest) -> AsyncGenerator[str, None]:
    """Yield SSE frames: a series of `token` events then a final `done` event."""
    session_uuid = _coerce_session(req.user_session_id)
    history = [m.model_dump() for m in req.chat_history]

    full_text = ""
    async for delta in copilot_chat(
        user_message=req.user_message,
        simulation_result=req.simulation_result,
        chat_history=history,
    ):
        full_text += delta
        yield _sse("token", {"delta": delta})

    formatted = format_response(req.user_message, req.simulation_result)
    formatted["ai_response"] = full_text.strip() or formatted["ai_response"]
    yield _sse("done", formatted)

    # Persist user + assistant turns in a fresh session (generator outlives request).
    async with SessionLocal() as session:
        session.add_all(
            [
                ChatMessage(
                    user_session_id=session_uuid,
                    role="user",
                    content=req.user_message,
                ),
                ChatMessage(
                    user_session_id=session_uuid,
                    role="assistant",
                    content=formatted["ai_response"],
                ),
            ]
        )
        await session.commit()
