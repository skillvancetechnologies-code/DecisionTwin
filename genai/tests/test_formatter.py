"""Formatter tests. Exercise the deterministic fallback (no live LLM needed)."""

from dt_genai.formatter import format_response, FormattedResponse, _heuristic_format

RAW = (
    "Raising prices by 10% would lift revenue about 6.8% while churn rises about "
    "2.1%.\n\n"
    "The main risk is that churn climbs, which hurts long-term retention.\n\n"
    "I recommend piloting the increase on one segment first. "
    "Want to compare this against a 5% increase?"
)


def test_format_response_returns_contract_keys():
    out = format_response(RAW)
    assert set(out.keys()) == {"summary", "recommendation", "risk_note", "follow_up_question"}


def test_follow_up_question_extracted():
    out = format_response(RAW)
    assert out["follow_up_question"].endswith("?")
    assert "5%" in out["follow_up_question"]


def test_summary_from_first_paragraph():
    fr = _heuristic_format(RAW)
    assert isinstance(fr, FormattedResponse)
    assert "revenue" in fr.summary.lower()


def test_web_backend_two_arg_call_style():
    # Backend calls format_response(user_message, simulation_result)
    sim = {"predicted_kpis": {"revenue_delta_pct": 6.8, "churn_delta_pct": 2.1},
           "risk_level": "Medium", "confidence_score": 80,
           "risk_factors": ["churn risk"]}
    out = format_response("Raise prices by 10%?", sim)
    assert "ai_response" in out  # required by chat_service
    assert set(out) >= {"ai_response", "summary", "recommendation", "risk_note"}
    assert "6.8" in out["ai_response"]


def test_handles_empty_and_single_line():
    out = format_response("Just one short line with no paragraphs.")
    assert out["summary"]
    assert out["recommendation"]
    assert out["risk_note"]
