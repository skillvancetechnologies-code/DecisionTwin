"""Output formatter (Section 6).

Public contract (Section 3.3):
    format_response(raw_llm_output: str) -> dict

Breaks the copilot's free-text explanation into structured fields used by the
dashboard, the DB, and the PDF report. Tries a fast second-pass LLM structuring
call; if the LLM is unavailable it falls back to a deterministic paragraph/
sentence split so the function always returns a valid object.
"""

import re
import json

from pydantic import BaseModel
from typing import Optional

from . import llm_client


class FormattedResponse(BaseModel):
    summary: str                       # 1-sentence TL;DR (paragraph 1)
    recommendation: str                # 1-sentence action (paragraph 3)
    risk_note: str                     # 1-sentence risk summary (paragraph 2)
    follow_up_question: Optional[str] = None


_STRUCTURE_PROMPT = (
    "Extract four fields from the business explanation and return ONLY JSON with "
    "keys: summary (1 sentence), recommendation (1 sentence), risk_note (1 "
    "sentence), follow_up_question (the question at the end, or null)."
)


def _first_sentence(text: str) -> str:
    text = text.strip()
    m = re.search(r"(.+?[.!?])(\s|$)", text)
    return (m.group(1) if m else text).strip()


def _heuristic_format(raw_text: str) -> FormattedResponse:
    """Deterministic fallback: split paragraphs / sentences."""
    raw_text = (raw_text or "").strip()
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", raw_text) if p.strip()]
    if len(paragraphs) < 3:
        # Fall back to sentence segmentation.
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", raw_text) if s.strip()]
        paragraphs = sentences or [raw_text]

    summary = _first_sentence(paragraphs[0]) if paragraphs else raw_text
    risk_note = _first_sentence(paragraphs[1]) if len(paragraphs) > 1 else ""
    recommendation = _first_sentence(paragraphs[2]) if len(paragraphs) > 2 else ""

    follow_up = None
    questions = re.findall(r"([^.?!\n]*\?)", raw_text)
    if questions:
        follow_up = questions[-1].strip()

    return FormattedResponse(
        summary=summary or raw_text[:200],
        recommendation=recommendation or "Review the simulation before acting.",
        risk_note=risk_note or "No specific risk factors were highlighted.",
        follow_up_question=follow_up,
    )


def format_response(*args) -> dict:
    """Structure a copilot response into structured fields.

    Two supported call styles (the second matches the Web backend's adapter):
      * format_response(raw_llm_output)               -> spec Section 6 fields
      * format_response(user_message, simulation_result) -> dict incl. ai_response
    """
    if len(args) >= 2:
        return _format_from_simulation(args[0], args[1])
    raw_llm_output = args[0] if args else ""
    try:
        messages = [
            llm_client.chat_message("system", _STRUCTURE_PROMPT),
            llm_client.chat_message("user", raw_llm_output),
        ]
        content = llm_client.complete(messages, temperature=0.0, max_tokens=300)
        # Strip code fences if present, then parse JSON.
        content = re.sub(r"^```(?:json)?|```$", "", content.strip(), flags=re.MULTILINE)
        data = json.loads(content)
        return FormattedResponse(**data).model_dump()
    except Exception:
        return _heuristic_format(raw_llm_output).model_dump()


def _format_from_simulation(user_message: str, simulation_result: dict | None) -> dict:
    """Web-backend call style: derive structured fields from a simulation.

    Returns a dict containing `ai_response` (a deterministic fallback the backend
    overrides with the streamed text) plus summary / recommendation / risk_note.
    """
    sim = simulation_result or {}
    kpis = sim.get("predicted_kpis", {}) or {}
    rev = kpis.get("revenue_delta_pct")
    churn = kpis.get("churn_delta_pct")
    risk = sim.get("risk_level", "Unknown")
    factors = ", ".join(sim.get("risk_factors", []) or []) or "the highlighted factors"

    rev_s = f"{rev:+.1f}%" if isinstance(rev, (int, float)) else "n/a"
    churn_s = f"{churn:+.1f}%" if isinstance(churn, (int, float)) else "n/a"

    ai_response = (
        f"Based on the simulation, this decision is predicted to move revenue by "
        f"{rev_s} and churn by {churn_s}. Overall risk is assessed as {risk}, "
        f"driven by {factors}."
    )
    recommendation = "Pilot the change on 1-2 segments and monitor the numbers before a full rollout."
    if (sim.get("confidence_score") or 100) < 60:
        recommendation = ("Treat these numbers as directional, not precise, and "
                          "proceed with caution via a limited pilot.")
    return {
        "ai_response": ai_response,
        "summary": f"Revenue {rev_s}, churn {churn_s}, {str(risk).lower()} risk.",
        "recommendation": recommendation,
        "risk_note": f"Watch for {factors}.",
    }


# --- Legacy helper kept for the existing FastAPI app --------------------

def enrich_analysis(category: str, risk: str, recommendation: str,
                    analysis_text: str) -> dict:
    """Risk-band enrichment used by app.py's /chat response."""
    return {
        "summary": f"{category} scenario detected. Risk Level: {risk}. {recommendation}",
        "formatted": analysis_text,
        "category": category,
        "risk_level": risk,
        "financial_impact": _financial_impact(risk),
        "operational_risk": _operational_risk(risk),
    }


def _financial_impact(risk):
    return {
        "Low": "Limited impact on profitability and cash flow.",
        "Medium": "Moderate impact on margins, operational spending, and growth projections.",
        "High": "Significant impact on profitability, liquidity, cash flow, and long-term business sustainability.",
    }.get(risk, "Financial impact unavailable.")


def _operational_risk(risk):
    return {
        "Low": "Minimal operational disruption expected.",
        "Medium": "Potential process inefficiencies, resource constraints, and execution delays.",
        "High": "High likelihood of operational bottlenecks, cash flow pressure, workforce strain, and supply chain disruption.",
    }.get(risk, "Operational risk unavailable.")
