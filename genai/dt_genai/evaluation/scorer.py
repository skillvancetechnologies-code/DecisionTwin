"""Applies the 5-axis rubric to a copilot response (Section 7).

The scorer is deterministic so it can run in CI with no LLM. It checks the
response text against the golden case's simulation_result. A meta-LLM scorer can
later pre-rank and a human spot-checks (Section 7.3); ``score_response`` is the
ground-truth heuristic used for regression gating.
"""

import re

from .rubric import RUBRIC, overall_pass, critical_pass

_ACTION_WORDS = re.compile(
    r"\b(recommend|consider|start|pilot|test|monitor|avoid|hold|proceed|"
    r"reconsider|reduce|increase|wait|run|review|re-?run)\b", re.I)
_JARGON = re.compile(r"\b(p-?value|stochastic|heteroskedastic|eigen|"
                     r"regression coefficient|confidence interval)\b", re.I)


def _kpi_numbers(sim: dict):
    """Headline KPI deltas the response would typically quote."""
    if not sim:
        return []
    kpis = sim.get("predicted_kpis", {}) or {}
    return [abs(round(v, 1)) for v in kpis.values() if isinstance(v, (int, float))]


def _allowed_numbers(sim: dict):
    """Every figure a response may legitimately cite (for hallucination check)."""
    if not sim:
        return []
    nums = _kpi_numbers(sim)
    for v in (sim.get("risk_score"), sim.get("confidence_score")):
        if isinstance(v, (int, float)):
            nums.append(abs(round(v, 1)))
    return nums


def _numbers_in_text(text: str):
    return [abs(float(n)) for n in re.findall(r"-?\d+(?:\.\d+)?", text)]


def _close(a, b, tol=0.6):
    return abs(a - b) <= tol


def score_response(case: dict, response: str) -> dict:
    sim = case.get("simulation_result")
    text = response or ""
    out_of_scope = case.get("out_of_scope")

    kpi_nums = _kpi_numbers(sim)
    resp_nums = _numbers_in_text(text)
    allowed = set(_allowed_numbers(sim))
    allowed |= set(_numbers_in_text(case.get("user_query", "")))  # query magnitude
    contradictions = [r for r in resp_nums if not any(_close(r, a) for a in allowed)]

    # --- Hallucination Check (binary) ---
    if out_of_scope:
        # any business number is fabricated in an off-topic reply
        hallucination = "FAIL" if resp_nums else "PASS"
    else:
        hallucination = "FAIL" if contradictions else "PASS"

    # --- Numerical Accuracy (cited numbers must be correct; quote the headline) ---
    if out_of_scope or not kpi_nums:
        numerical = 5  # nothing to cite; correctness is "don't invent"
    elif contradictions:
        numerical = 2  # cited a number that doesn't match the simulation
    else:
        headline = kpi_nums[0]  # revenue_delta_pct
        numerical = 5 if any(_close(headline, r) for r in resp_nums) else 3

    # --- Risk Honesty ---
    factors = (sim or {}).get("risk_factors", []) if sim else []
    if out_of_scope or not factors:
        risk_honesty = 5
    else:
        lowered = text.lower()
        # match on the salient word of each factor
        hits = 0
        for f in factors:
            words = [w for w in re.findall(r"[a-z]{4,}", f.lower())]
            if any(w in lowered for w in words):
                hits += 1
        risk_honesty = round(5 * hits / len(factors))

    # --- Tone & Clarity ---
    words = len(text.split())
    tone = 5
    if words > 320 or words < 8:
        tone -= 2
    if re.search(r"^\s*[-*•]", text, re.M):  # bullet points discouraged
        tone -= 1
    if _JARGON.search(text):
        tone -= 1
    tone = max(0, min(5, tone))

    # --- Recommendation Soundness ---
    if out_of_scope:
        recommendation = 5  # a clean redirect is the correct "action" here
    else:
        recommendation = 5 if _ACTION_WORDS.search(text) else 2
    if case.get("low_confidence") and "caution" not in text.lower() \
            and "directional" not in text.lower():
        recommendation = min(recommendation, 3)

    scores = {
        "numerical_accuracy": numerical,
        "recommendation_soundness": recommendation,
        "tone_clarity": tone,
        "risk_honesty": risk_honesty,
        "hallucination_check": hallucination,
    }
    return {
        "scores": scores,
        "passed": overall_pass(scores),
        "critical_passed": critical_pass(scores),
        "failed_axes": [RUBRIC[k].name for k, v in scores.items()
                        if not _axis_ok(k, v)],
    }


def _axis_ok(key, value):
    from .rubric import axis_passed
    return axis_passed(RUBRIC[key], value)


# --- Optional meta-LLM scorer hook (Section 7.3) -----------------------

def llm_prescore(case: dict, response: str):
    """Placeholder for an LLM pre-ranker; returns None if no LLM configured."""
    return None
