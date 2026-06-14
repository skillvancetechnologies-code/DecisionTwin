"""Copilot tests. With no LLM key these exercise the graceful fallback path."""

import asyncio

import dt_genai
from dt_genai import copilot
from dt_genai import memory


def test_chat_is_async_generator_yielding_strings():
    async def go():
        chunks = [c async for c in dt_genai.chat("Raise prices by 10%?")]
        return chunks
    chunks = asyncio.run(go())
    assert chunks and all(isinstance(c, str) for c in chunks)


def test_chat_complete_returns_string():
    out = asyncio.run(copilot.chat_complete("Hire 5 engineers?"))
    assert isinstance(out, str) and out


def test_chat_records_to_memory():
    memory.clear_memory()
    asyncio.run(copilot.chat_complete("Cut marketing by 20%?"))
    hist = memory.get_memory()
    assert hist[-2]["role"] == "user"
    assert hist[-1]["role"] == "assistant"


def test_build_messages_injects_simulation_and_low_confidence_note():
    msgs = copilot._build_messages(
        "Raise prices by 10%",
        {"confidence_score": 40, "predicted_kpis": {"revenue_delta_pct": 6.8}},
        None,
    )
    joined = " ".join(m["content"] for m in msgs)
    assert "SIMULATION_RESULT" in joined
    assert "directional" in joined  # low-confidence guidance injected
