"""PDF report generator tests."""

import dt_genai
from dt_genai.report_generator import build_pdf, generate_report

SCENARIO = {
    "name": "Pricing +10%",
    "user_query": "Raise prices by 10%?",
    "result": {
        "predicted_kpis": {"revenue_delta_pct": 6.8, "churn_delta_pct": 2.1,
                           "growth_rate_new": 4.5},
        "risk_level": "Medium", "confidence_score": 72, "model_used": "open-mistral-7b",
    },
    "formatted": {"summary": "Revenue up ~6.8%.", "risk_note": "Churn may rise.",
                  "recommendation": "Pilot on one segment first."},
}


def test_build_pdf_returns_pdf_bytes():
    pdf = dt_genai.build_pdf(SCENARIO)
    assert isinstance(pdf, bytes)
    assert pdf[:4] == b"%PDF"
    assert len(pdf) > 800


def test_build_pdf_tolerates_missing_fields():
    pdf = build_pdf({"name": "Bare", "user_query": "x?", "result": {}})
    assert pdf[:4] == b"%PDF"


def test_build_pdf_backend_scenario_shape():
    # Shape the Web backend's scenarios_service passes (ai_explanation, no "formatted")
    pdf = build_pdf({
        "name": "Pricing +10%", "user_query": "Raise prices by 10%?",
        "decision_type": "price_change",
        "result": {"predicted_kpis": {"revenue_delta_pct": 6.8, "churn_delta_pct": 2.1,
                                      "growth_rate_new": 4.5},
                   "risk_level": "Medium", "risk_score": 54, "confidence_score": 72},
        "ai_explanation": "Revenue would rise about 6.8%. The main risk is churn. "
                          "I recommend a pilot first.",
    })
    assert pdf[:4] == b"%PDF" and len(pdf) > 800


def test_generate_report_text_contains_query():
    txt = generate_report({
        "user_query": "Raise prices by 10%?",
        "parsed_query": {"decision_type": "price_change"},
        "ml_route": "pricing_model", "decision_score": 12.0,
        "simulation_result": {"revenue_change": 6.8, "profit_change": 4.0, "risk_score": 0.5},
        "ai_recommendation": "Proceed with a pilot.",
    })
    assert "Raise prices by 10%?" in txt
    assert "price_change" in txt
