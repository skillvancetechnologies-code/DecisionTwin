"""Copilot: streaming chat() async generator + conversation memory (Section 5).

Public contract (Section 3.3):
    chat(message, simulation_result, history) -> async generator of str chunks

Provider: Mistral (open-mistral-7b) per PM decision. The Mistral SDK is
synchronous, so the streaming call is run in a worker thread and its chunks are
re-yielded asynchronously to satisfy the documented async-generator contract.
"""

import json
import asyncio
from typing import AsyncIterator

from .prompts import SYSTEM_COPILOT_PROMPT
from . import llm_client
from .memory import get_memory, add_to_memory

# --- Static fallbacks (Section 5.4) -------------------------------------

NEED_SIMULATION = (
    "I need a fresh simulation to answer that. Could you rephrase as a specific "
    "change - e.g. raise prices by X% - so I can run the model?"
)
OUT_OF_SCOPE = (
    "I'm focused on simulating business decisions. I can't help with that, but I "
    "can help you simulate pricing, hiring, or marketing changes."
)
API_DOWN = (
    "Sorry - I'm having trouble reaching the analysis engine right now. "
    "Please try again in a moment."
)


def _build_messages(user_message, simulation_result, chat_history):
    messages = [llm_client.chat_message("system", SYSTEM_COPILOT_PROMPT)]
    if simulation_result:
        confidence = simulation_result.get("confidence_score")
        if confidence is not None and confidence < 50:
            messages.append(llm_client.chat_message(
                "system",
                "Note: confidence is low; begin your reply by telling the user to "
                "treat the numbers as directional, not precise.",
            ))
        messages.append(llm_client.chat_message(
            "system",
            f"SIMULATION_RESULT:\n{json.dumps(simulation_result, indent=2)}",
        ))
    for msg in (chat_history or []):
        messages.append(llm_client.chat_message(msg["role"], msg["content"]))
    messages.append(llm_client.chat_message("user", user_message))
    return messages


async def chat(
    user_message: str,
    simulation_result: dict | None = None,
    chat_history: list[dict] | None = None,
) -> AsyncIterator[str]:
    """Stream the copilot's response token-by-token.

    Yields str chunks. Falls back to a static message if the LLM is unavailable.
    """
    messages = _build_messages(user_message, simulation_result, chat_history)

    queue: asyncio.Queue = asyncio.Queue()
    loop = asyncio.get_event_loop()
    _DONE = object()

    def _produce():
        try:
            for delta in llm_client.stream(messages):
                loop.call_soon_threadsafe(queue.put_nowait, delta)
        except llm_client.LLMUnavailable:
            loop.call_soon_threadsafe(queue.put_nowait, API_DOWN)
        except Exception:
            loop.call_soon_threadsafe(queue.put_nowait, API_DOWN)
        finally:
            loop.call_soon_threadsafe(queue.put_nowait, _DONE)

    task = loop.run_in_executor(None, _produce)
    collected = []
    while True:
        chunk = await queue.get()
        if chunk is _DONE:
            break
        collected.append(chunk)
        yield chunk
    await task

    add_to_memory("user", user_message)
    add_to_memory("assistant", "".join(collected))


async def chat_complete(user_message, simulation_result=None, chat_history=None) -> str:
    """Convenience: collect the full streamed response into a single string."""
    parts = [c async for c in chat(user_message, simulation_result, chat_history)]
    return "".join(parts)


async def generate_chat_response(user_message, business_result=None) -> str:
    """Backwards-compatible entry point used by app.py (non-streaming).

    Uses recent memory for context and degrades gracefully when the LLM is down.
    """
    history = get_memory()[-2:]
    try:
        messages = [llm_client.chat_message("system", SYSTEM_COPILOT_PROMPT)]
        for msg in history:
            messages.append(llm_client.chat_message(msg["role"], msg["content"]))
        messages.append(llm_client.chat_message("user", user_message))
        ai_response = llm_client.complete(messages, temperature=0.2)
    except llm_client.LLMUnavailable:
        if business_result:
            ai_response = (
                f"Business Analysis\n- Category: {business_result.get('category')}\n"
                f"- Risk Level: {business_result.get('risk')}\n\n"
                f"Recommendation\n- {business_result.get('recommendation')}"
            )
        else:
            ai_response = API_DOWN

    add_to_memory("user", user_message)
    add_to_memory("assistant", ai_response)
    return ai_response
