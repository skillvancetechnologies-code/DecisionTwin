"""Evaluation framework tests: rubric gates + scorer behavior."""

from dt_genai.evaluation import GOLDEN_SET, score_response
from dt_genai.evaluation.rubric import RUBRIC, overall_pass, critical_pass

GOOD = (
    "Raising prices by 10% would lift revenue about 6.8% while churn rises about "
    "2.1% and growth reaches about 4.5%. The key risks are churn risk and "
    "competitor response, which could pressure retention. I recommend a small "
    "pilot and monitoring the numbers. Want to compare against a 5% increase?"
)
CASE = next(c for c in GOLDEN_SET if c["id"] == 2)  # price +10%


def test_golden_set_has_25_cases_and_buckets():
    assert len(GOLDEN_SET) == 25
    buckets = {c["bucket"] for c in GOLDEN_SET}
    assert {"price", "headcount", "marketing", "edge", "multiturn",
            "out_of_scope", "missing_data"} <= buckets


def test_rubric_has_five_axes_with_two_critical():
    assert len(RUBRIC) == 5
    assert sum(1 for a in RUBRIC.values() if a.critical) == 3  # num, risk, halluc


def test_good_response_passes_all_axes():
    result = score_response(CASE, GOOD)
    assert result["passed"], result["failed_axes"]


def test_invented_number_fails_hallucination_gate():
    bad = GOOD + " Also, profit will jump exactly 99.7% next week."
    result = score_response(CASE, bad)
    assert result["scores"]["hallucination_check"] == "FAIL"
    assert not result["passed"]


def test_dropped_risk_factor_fails_risk_honesty():
    # omit both risk factors entirely
    no_risk = ("Raising prices by 10% lifts revenue about 6.8% and churn about "
               "2.1%. I recommend a pilot. Want to compare to 5%?")
    result = score_response(CASE, no_risk)
    assert result["scores"]["risk_honesty"] < 5


def test_out_of_scope_with_numbers_is_hallucination():
    case = next(c for c in GOLDEN_SET if c.get("out_of_scope"))
    result = score_response(case, "Sure, your IRR will be about 12.5%.")
    assert result["scores"]["hallucination_check"] == "FAIL"


def test_overall_and_critical_pass_helpers():
    perfect = {"numerical_accuracy": 5, "recommendation_soundness": 4,
               "tone_clarity": 4, "risk_honesty": 5, "hallucination_check": "PASS"}
    assert overall_pass(perfect) and critical_pass(perfect)
    weak_noncritical = {**perfect, "tone_clarity": 2}
    assert not overall_pass(weak_noncritical)
    assert critical_pass(weak_noncritical)  # criticals still fine
