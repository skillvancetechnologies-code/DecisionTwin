"""PDF report generator (Section 8).

Public contract (Section 3.3):
    build_pdf(scenario: dict) -> bytes

Single-page, presentation-ready scenario report built with reportlab Platypus.
Also keeps ``generate_report`` (plain text) used by the simulation pipeline.
"""

from io import BytesIO
from datetime import date


def _fmt_pct(value):
    try:
        return f"{float(value):+.1f}%"
    except (TypeError, ValueError):
        return "n/a"


def _get(d, *keys, default=None):
    for k in keys:
        if isinstance(d, dict) and k in d and d[k] is not None:
            return d[k]
    return default


def build_pdf(scenario: dict) -> bytes:
    """Render a one-page scenario PDF and return the raw bytes."""
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer)
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    from reportlab.lib.units import mm

    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=40, rightMargin=40,
                            topMargin=50, bottomMargin=50,
                            title="DecisionTwin Scenario Report")
    styles = getSampleStyleSheet()
    story = []

    result = scenario.get("result", {}) or {}
    kpis = result.get("predicted_kpis", {}) or {}
    # Body fields: prefer an explicit "formatted" block; otherwise derive them
    # from the ai_explanation text the Web backend passes.
    formatted = scenario.get("formatted") or {}
    if not formatted and scenario.get("ai_explanation"):
        from .formatter import _heuristic_format
        formatted = _heuristic_format(scenario["ai_explanation"]).model_dump()

    # --- Header band ---
    story.append(Paragraph("<b>DecisionTwin Scenario Report</b>", styles["Title"]))
    story.append(Paragraph(scenario.get("name", "Untitled Scenario"), styles["Heading2"]))
    story.append(Paragraph(date.today().isoformat(), styles["Normal"]))
    story.append(Spacer(1, 12))

    # --- KPI strip (4 cards) ---
    kpi_row = [
        f"Revenue\n{_fmt_pct(_get(kpis, 'revenue_delta_pct'))}",
        f"Churn\n{_fmt_pct(_get(kpis, 'churn_delta_pct'))}",
        f"Growth\n{_fmt_pct(_get(kpis, 'growth_rate_new'))}",
        f"Risk\n{_get(result, 'risk_level', default='n/a')}",
    ]
    kpi_table = Table([kpi_row], colWidths=[(A4[0] - 80) / 4.0] * 4)
    kpi_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#1b2a4a")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#1b2a4a")),
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#eef1f6")),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 18))

    # --- The Question ---
    story.append(Paragraph("<b>The Question</b>", styles["Heading3"]))
    story.append(Paragraph(f"<i>{scenario.get('user_query', '')}</i>", styles["Normal"]))
    if scenario.get("decision_type"):
        story.append(Paragraph(f"Decision type: {scenario['decision_type']}", styles["Normal"]))
    story.append(Spacer(1, 10))

    # --- Executive Summary ---
    story.append(Paragraph("<b>Executive Summary</b>", styles["Heading3"]))
    story.append(Paragraph(_get(formatted, "summary", default="-"), styles["Normal"]))
    story.append(Spacer(1, 10))

    # --- Risk Note ---
    story.append(Paragraph("<b>Risk Note</b>", styles["Heading3"]))
    story.append(Paragraph(_get(formatted, "risk_note", default="-"), styles["Normal"]))
    story.append(Spacer(1, 10))

    # --- Recommendation ---
    story.append(Paragraph("<b>Recommendation</b>", styles["Heading3"]))
    story.append(Paragraph(_get(formatted, "recommendation", default="-"), styles["Normal"]))
    story.append(Spacer(1, 16))

    # --- Confidence + Methodology footer ---
    confidence = _get(result, "confidence_score", default="n/a")
    model_used = _get(result, "model_used", default="open-mistral-7b")
    footer = (f"Confidence: {confidence} &nbsp;|&nbsp; Model: {model_used} "
              f"&nbsp;|&nbsp; Generated: {date.today().isoformat()}")
    story.append(Paragraph(footer, styles["Italic"]))

    doc.build(story)
    return buf.getvalue()


def generate_report(result) -> str:
    """Plain-text decision report used by dt_genai.pipeline."""
    sim = result.get("simulation_result", {})
    return f"""Business Decision Report
========================

User Query:
{result.get("user_query", "")}

Decision Type:
{result.get("parsed_query", {}).get("decision_type", "")}

ML Route:
{result.get("ml_route", "")}

Decision Score:
{result.get("decision_score", "")}

Simulation Results
------------------
Revenue Change: {sim.get("revenue_change", "")}
Profit Change: {sim.get("profit_change", "")}
Risk Score: {sim.get("risk_score", "")}

Recommendation
--------------
{result.get("ai_recommendation", "")}
"""
