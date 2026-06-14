"""Stage-2 LLM fallback parser (Section 4.3).

Used by query_parser.parse() when the rule-based pass returns None. Uses the
Mistral client with a strict JSON instruction (open-mistral-7b function-calling
support is limited, so we instruct-and-validate rather than tool-call) and
validates the result against ParsedQuery. Returns None if the LLM is
unavailable or the output fails validation, so the caller can fall back to a
clarification response.
"""

import re
import json

from .schemas import ParsedQuery
from .prompts.system_parser import SYSTEM_PARSER_PROMPT
from . import llm_client


def llm_parse(text: str):
    try:
        messages = [
            llm_client.chat_message("system", SYSTEM_PARSER_PROMPT),
            llm_client.chat_message("user", text),
        ]
        content = llm_client.complete(messages, temperature=0.0, max_tokens=200)
    except llm_client.LLMUnavailable:
        return None

    content = re.sub(r"^```(?:json)?|```$", "", content.strip(), flags=re.MULTILINE)
    try:
        data = json.loads(content)
    except (ValueError, TypeError):
        return None

    data.setdefault("target_metric", None)
    data["parser_used"] = "llm"
    data["raw_query"] = text
    try:
        return ParsedQuery(**data)
    except Exception:
        return None
