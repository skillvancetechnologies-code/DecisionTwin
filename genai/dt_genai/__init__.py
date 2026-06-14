"""dt_genai package public API.

Per Section 3.3 of the execution document the Web backend imports these four
stable public functions. Any change to their signatures is a [CONTRACT] change.

    parse(user_message)                      -> ParsedQuery     (AI-2)
    chat(message, sim_result, history)       -> async generator (AI-1)
    format_response(raw_llm_output)          -> dict            (AI-1)
    build_pdf(scenario)                      -> bytes           (AI-2)
"""

from .query_parser import parse
from .copilot import chat
from .formatter import format_response
from .report_generator import build_pdf

__all__ = ["parse", "chat", "format_response", "build_pdf"]
