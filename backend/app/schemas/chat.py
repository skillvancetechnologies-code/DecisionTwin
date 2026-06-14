"""Schemas for the /chat streaming endpoint."""
from typing import Any

from pydantic import BaseModel


class ChatMessageIn(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    user_session_id: str
    user_message: str
    simulation_result: dict[str, Any] | None = None
    chat_history: list[ChatMessageIn] = []
