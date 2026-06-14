"""Evaluation framework (Section 7): 5-axis rubric, scorer, and golden set."""

from .rubric import RUBRIC, AXES
from .scorer import score_response
from .golden_set import GOLDEN_SET

__all__ = ["RUBRIC", "AXES", "score_response", "GOLDEN_SET"]
