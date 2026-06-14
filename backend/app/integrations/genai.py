"""Adapter over the GenAI team's `dt_genai` package.

Falls back to a deterministic reference copilot when `dt_genai` is not
installed, so chat streaming and PDF reports work without an LLM key during
development. Public surface mirrors the documented contract:

    parse_query(text) -> dict
    copilot_chat(user_message, simulation_result, chat_history) -> async generator
    format_response(...) -> dict
    build_pdf(scenario) -> bytes
"""
from __future__ import annotations

import re
from collections.abc import AsyncGenerator
from io import BytesIO
from typing import Any

try:  # Production: real GenAI package
    from dt_genai.query_parser import parse as _dt_parse  # type: ignore
    from dt_genai.copilot import chat as copilot_chat  # type: ignore
    from dt_genai.formatter import format_response  # type: ignore
    from dt_genai.report_generator import build_pdf  # type: ignore

    USING_REAL_GENAI = True

    def parse_query(user_message: str) -> dict:
        """Normalize dt_genai's ParsedQuery model to the documented dict contract."""
        result = _dt_parse(user_message)
        return result.model_dump() if hasattr(result, "model_dump") else dict(result)
except ImportError:
    USING_REAL_GENAI = False

    def parse_query(user_message: str) -> dict:
        text = user_message.lower()
        if any(w in text for w in ("hire", "headcount", "staff", "engineer")):
            decision_type = "headcount"
        elif any(w in text for w in ("marketing", "ad", "campaign", "spend")):
            decision_type = "marketing"
        else:
            decision_type = "price_change"
        match = re.search(r"(-?\d+(?:\.\d+)?)\s*%?", text)
        magnitude = float(match.group(1)) if match else 10.0
        return {
            "decision_type": decision_type,
            "parameter": "price_per_unit"
            if decision_type == "price_change"
            else decision_type,
            "magnitude": magnitude,
            "magnitude_type": "percentage",
            "confidence": 0.7,
        }

    def format_response(
        user_message: str, simulation_result: dict | None
    ) -> dict:
        sim = simulation_result or {}
        kpis = sim.get("predicted_kpis", {})
        rev = kpis.get("revenue_delta_pct", 0)
        churn = kpis.get("churn_delta_pct", 0)
        risk = sim.get("risk_level", "Unknown")
        ai_response = (
            f"Based on the simulation, this decision is predicted to move revenue "
            f"by {rev:+.1f}% and churn by {churn:+.1f}%. Overall risk is assessed "
            f"as {risk}."
        )
        return {
            "ai_response": ai_response,
            "summary": f"Revenue {rev:+.1f}%, churn {churn:+.1f}%, {str(risk).lower()} risk.",
            "recommendation": "Pilot in 1-2 segments before a full rollout.",
            "risk_note": "Watch for churn in price-sensitive segments.",
        }

    async def copilot_chat(
        user_message: str,
        simulation_result: dict | None = None,
        chat_history: list[dict] | None = None,
    ) -> AsyncGenerator[str, None]:
        formatted = format_response(user_message, simulation_result)
        for word in formatted["ai_response"].split(" "):
            yield word + " "

    def build_pdf(scenario: dict[str, Any]) -> bytes:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.units import inch
        from reportlab.pdfgen import canvas

        buf = BytesIO()
        pdf = canvas.Canvas(buf, pagesize=letter)
        width, height = letter
        y = height - inch

        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawString(inch, y, "DecisionTwin — Scenario Report")
        y -= 0.4 * inch
        pdf.setFont("Helvetica", 11)

        def line(label: str, value: Any) -> None:
            nonlocal y
            pdf.drawString(inch, y, f"{label}: {value}")
            y -= 0.28 * inch

        line("Scenario", scenario.get("name", "Untitled"))
        line("Query", scenario.get("user_query", ""))
        line("Decision type", scenario.get("decision_type", ""))

        result = scenario.get("result", {})
        kpis = result.get("predicted_kpis", {})
        line("Revenue delta %", kpis.get("revenue_delta_pct", "-"))
        line("Churn delta %", kpis.get("churn_delta_pct", "-"))
        line("Risk level", result.get("risk_level", "-"))
        line("Risk score", result.get("risk_score", "-"))
        line("Confidence", result.get("confidence_score", "-"))

        y -= 0.2 * inch
        pdf.setFont("Helvetica-Oblique", 10)
        explanation = (scenario.get("ai_explanation") or "")[:600]
        for chunk in [explanation[i : i + 90] for i in range(0, len(explanation), 90)]:
            pdf.drawString(inch, y, chunk)
            y -= 0.22 * inch

        pdf.showPage()
        pdf.save()
        return buf.getvalue()
