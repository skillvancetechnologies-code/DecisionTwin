"""Mistral client wrapper: lazy init, retries, logging.

The client is created lazily so the package imports cleanly even when
``mistralai`` is not installed or no API key is set (e.g. in CI / unit tests).
Provider is Mistral (open-mistral-7b) per the PM decision.
"""

import os
import time
import logging

logger = logging.getLogger("dt_genai.llm")

DEFAULT_MODEL = "open-mistral-7b"

_client = None


class LLMUnavailable(RuntimeError):
    """Raised when the LLM cannot be reached or is not configured."""


def get_client():
    """Return a cached MistralClient, or raise LLMUnavailable."""
    global _client
    if _client is not None:
        return _client
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except Exception:
        pass
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise LLMUnavailable("MISTRAL_API_KEY not set")
    try:
        from mistralai.client import MistralClient
    except Exception as exc:  # pragma: no cover - depends on env
        raise LLMUnavailable(f"mistralai not installed: {exc}") from exc
    _client = MistralClient(api_key=api_key)
    return _client


def chat_message(role: str, content: str) -> dict:
    """Build a provider-agnostic message dict.

    Kept SDK-free so callers can construct messages without ``mistralai``
    installed; the dicts are converted to ChatMessage inside the client.
    """
    return {"role": role, "content": content}


def _to_sdk_messages(messages):
    from mistralai.models.chat_completion import ChatMessage
    return [ChatMessage(role=m["role"], content=m["content"]) for m in messages]


def complete(messages, model: str = DEFAULT_MODEL, temperature: float = 0.4,
             max_tokens: int = 600, retries: int = 3):
    """Non-streaming completion with exponential backoff (1s, 2s, 4s)."""
    client = get_client()
    sdk_messages = _to_sdk_messages(messages)
    delay = 1.0
    last_exc = None
    for attempt in range(retries):
        try:
            resp = client.chat(model=model, messages=sdk_messages,
                               temperature=temperature, max_tokens=max_tokens)
            return resp.choices[0].message.content
        except Exception as exc:  # rate limit / timeout / transient
            last_exc = exc
            logger.warning("LLM call failed (attempt %d/%d): %s",
                           attempt + 1, retries, exc)
            if attempt < retries - 1:
                time.sleep(delay)
                delay *= 2
    raise LLMUnavailable(f"LLM failed after {retries} attempts: {last_exc}")


def stream(messages, model: str = DEFAULT_MODEL, temperature: float = 0.4,
           max_tokens: int = 600):
    """Yield text chunks from a streaming completion."""
    client = get_client()
    sdk_messages = _to_sdk_messages(messages)
    for chunk in client.chat_stream(model=model, messages=sdk_messages,
                                    temperature=temperature, max_tokens=max_tokens):
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta
