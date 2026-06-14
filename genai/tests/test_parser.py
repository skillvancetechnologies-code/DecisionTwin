"""Parser test suite.

Covers the required cases from Section 4.4 of the execution document plus
extra coverage for negatives, percentages, absolute values, money suffixes,
ambiguous/clarification cases and off-topic queries.

Run:  pytest -k parser -v
"""

import pytest

from dt_genai.query_parser import parse

# (query, expected_decision_type, expected_magnitude, expected_magnitude_type)
# magnitude/type of None means "don't assert" (ambiguous/clarification case).
CASES = [
    ("Raise prices by 10%", "price_change", 10, "percentage"),
    ("What if we cut prices 5 dollars?", "price_change", -5, "absolute"),
    ("Bump prices a little", "price_change", None, None),
    ("Hire 5 more engineers", "headcount", 5, "absolute"),
    ("Lay off 3 sales reps", "headcount", -3, "absolute"),
    ("Grow the team by 20%", "headcount", 20, "percentage"),
    ("Cut marketing by 25%", "marketing", -25, "percentage"),
    ("Double our ad spend", "marketing", 100, "percentage"),
    ("Reduce marketing spend by $10K", "marketing", -10000, "absolute"),
    ("Open a new branch in Mumbai", "other", None, None),
    ("What's our churn rate?", "other", None, None),
    ("Should we drop prices to fight competitor X?", "price_change", None, None),
    # extra coverage
    ("Increase prices by 15 percent", "price_change", 15, "percentage"),
    ("decrease price by 8%", "price_change", -8, "percentage"),
    ("hire 10 employees", "headcount", 10, "absolute"),
    ("fire 2 staff", "headcount", -2, "absolute"),
    ("increase marketing by 30%", "marketing", 30, "percentage"),
    ("Predict the stock market", "other", None, None),
]


@pytest.mark.parametrize("query,decision_type,magnitude,magnitude_type", CASES)
def test_parse_cases(query, decision_type, magnitude, magnitude_type):
    result = parse(query)
    assert result.decision_type == decision_type, f"{query!r} -> {result.decision_type}"
    if magnitude is not None:
        assert result.magnitude == magnitude, f"{query!r} magnitude={result.magnitude}"
    if magnitude_type is not None:
        assert result.magnitude_type == magnitude_type


def test_raw_query_preserves_original_text():
    q = "Raise PRICES by 10%"
    assert parse(q).raw_query == q


def test_confidence_in_range():
    for query, *_ in CASES:
        c = parse(query).confidence
        assert 0.0 <= c <= 1.0


def test_ambiguous_price_is_low_confidence():
    # "a little" has no magnitude -> should flag for clarification (low confidence)
    assert parse("Bump prices a little").confidence < 0.5


def test_off_topic_is_other_zero_confidence():
    r = parse("Open a new branch in Mumbai")
    assert r.decision_type == "other"
    assert r.confidence == 0.0
