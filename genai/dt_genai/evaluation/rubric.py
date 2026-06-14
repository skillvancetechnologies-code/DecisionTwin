"""The 5-axis AI response evaluation rubric (Section 7.1).

Each axis defines how a copilot response is scored and the threshold required to
"pass". Numerical Accuracy and Risk Honesty are hard gates (5/5 and PASS
respectively); a single failure on those should block a demo.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Axis:
    key: str
    name: str
    measures: str
    kind: str          # "0-5" or "binary"
    pass_threshold: float | str
    critical: bool     # critical axes must pass before any demo


AXES = [
    Axis("numerical_accuracy", "Numerical Accuracy",
         "Do the numbers in the explanation match the simulation_result JSON?",
         "0-5", 5, True),
    Axis("recommendation_soundness", "Recommendation Soundness",
         "Is the recommendation actionable and justified by the data?",
         "0-5", 4, False),
    Axis("tone_clarity", "Tone & Clarity",
         "Plain English? No jargon? Reads in 30 seconds?",
         "0-5", 4, False),
    Axis("risk_honesty", "Risk Honesty",
         "Does it surface the actual risk factors from the JSON?",
         "0-5", 5, True),
    Axis("hallucination_check", "Hallucination Check",
         "Are there any claims not supported by the inputs?",
         "binary", "PASS", True),
]

# Convenience lookups
RUBRIC = {axis.key: axis for axis in AXES}


def axis_passed(axis: Axis, value) -> bool:
    if axis.kind == "binary":
        return str(value).upper() == "PASS"
    return value >= axis.pass_threshold


def overall_pass(scores: dict) -> bool:
    """A response passes only if every axis meets its threshold."""
    return all(axis_passed(RUBRIC[k], scores.get(k)) for k in RUBRIC)


def critical_pass(scores: dict) -> bool:
    """Demo gate: every critical axis must pass (others may be borderline)."""
    return all(axis_passed(RUBRIC[k], scores.get(k))
               for k in RUBRIC if RUBRIC[k].critical)
