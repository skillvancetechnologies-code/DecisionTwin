"""The 25-case golden set (Section 7.2).

Buckets: vanilla price (5), headcount (4), marketing (4), edge cases (4),
multi-turn refinements (4), out-of-scope (2), missing-data (2).

Each case carries the simulation_result the copilot would receive plus the
"truth" the scorer checks against: numbers that must appear and the risk
factors that must be surfaced.
"""


def _sim(rev, churn, growth, risk_level, risk_score, conf, factors):
    return {
        "predicted_kpis": {
            "revenue_delta_pct": rev,
            "churn_delta_pct": churn,
            "growth_rate_new": growth,
        },
        "risk_level": risk_level,
        "risk_score": risk_score,
        "confidence_score": conf,
        "risk_factors": factors,
    }


GOLDEN_SET = [
    # --- Vanilla price changes (5) ---
    {"id": 1, "bucket": "price", "user_query": "What if I raise prices by 5%?",
     "simulation_result": _sim(3.4, 1.2, 4.0, "Low", 28, 84, ["minor churn uptick"])},
    {"id": 2, "bucket": "price", "user_query": "Raise prices by 10%.",
     "simulation_result": _sim(6.8, 2.1, 4.5, "Medium", 54, 80, ["churn risk", "competitor response"])},
    {"id": 3, "bucket": "price", "user_query": "Increase prices by 25%.",
     "simulation_result": _sim(14.0, 7.5, 3.0, "High", 78, 71, ["sharp churn", "demand drop"])},
    {"id": 4, "bucket": "price", "user_query": "Cut prices by 5%.",
     "simulation_result": _sim(-2.1, -1.0, 6.0, "Low", 22, 83, ["margin pressure"])},
    {"id": 5, "bucket": "price", "user_query": "Lower prices by 15%.",
     "simulation_result": _sim(-6.0, -2.5, 9.0, "Medium", 48, 77, ["margin erosion", "price-war risk"])},

    # --- Headcount changes (4) ---
    {"id": 6, "bucket": "headcount", "user_query": "Hire 5 more engineers.",
     "simulation_result": _sim(2.5, 0.0, 5.0, "Medium", 40, 82, ["payroll cost", "ramp-up time"])},
    {"id": 7, "bucket": "headcount", "user_query": "Add 10 sales reps.",
     "simulation_result": _sim(8.0, -0.5, 7.0, "Medium", 45, 79, ["ramp cost", "quota risk"])},
    {"id": 8, "bucket": "headcount", "user_query": "Lay off 3 ops staff.",
     "simulation_result": _sim(0.5, 1.5, -1.0, "High", 62, 74, ["service degradation", "morale impact"])},
    {"id": 9, "bucket": "headcount", "user_query": "Grow the team by 50%.",
     "simulation_result": _sim(6.0, 0.0, 8.0, "High", 70, 66, ["burn-rate spike", "management strain"])},

    # --- Marketing budget changes (4) ---
    {"id": 10, "bucket": "marketing", "user_query": "Increase marketing by 30%.",
     "simulation_result": _sim(5.5, -1.0, 9.0, "Medium", 44, 80, ["diminishing returns"])},
    {"id": 11, "bucket": "marketing", "user_query": "Cut marketing by 20%.",
     "simulation_result": _sim(-3.0, 1.2, -4.0, "Medium", 50, 78, ["pipeline shrink"])},
    {"id": 12, "bucket": "marketing", "user_query": "Reduce marketing by 50%.",
     "simulation_result": _sim(-9.0, 3.0, -11.0, "High", 75, 70, ["lead-gen collapse", "brand decay"])},
    {"id": 13, "bucket": "marketing", "user_query": "Add $100K to marketing.",
     "simulation_result": _sim(4.0, -0.8, 6.5, "Low", 30, 81, ["attribution uncertainty"])},

    # --- Edge cases (4) ---
    {"id": 14, "bucket": "edge", "user_query": "Raise prices by 200%.",
     "simulation_result": _sim(20.0, 45.0, -30.0, "High", 96, 58, ["mass churn", "demand collapse"])},
    {"id": 15, "bucket": "edge", "user_query": "Cut marketing by 90%.",
     "simulation_result": _sim(-18.0, 6.0, -25.0, "High", 92, 60, ["pipeline collapse"])},
    {"id": 16, "bucket": "edge", "user_query": "Hire 1000 engineers.",
     "simulation_result": _sim(3.0, 0.0, 5.0, "High", 90, 41, ["unsustainable burn", "low confidence"])},
    {"id": 17, "bucket": "edge", "user_query": "What if we change nothing (0%)?",
     "simulation_result": _sim(0.0, 0.0, 2.0, "Low", 15, 88, ["status quo drift"])},

    # --- Multi-turn refinements (4) ---
    {"id": 18, "bucket": "multiturn", "user_query": "But what about churn if I do that?",
     "history": [{"role": "user", "content": "Raise prices by 10%."},
                 {"role": "assistant", "content": "Revenue would rise about 6.8%..."}],
     "simulation_result": _sim(6.8, 2.1, 4.5, "Medium", 54, 80, ["churn risk"])},
    {"id": 19, "bucket": "multiturn", "user_query": "What if I only raise by 5% instead?",
     "history": [{"role": "user", "content": "Raise prices by 10%."},
                 {"role": "assistant", "content": "Revenue up ~6.8%, churn up ~2.1%."}],
     "simulation_result": _sim(3.4, 1.2, 4.0, "Low", 28, 84, ["minor churn uptick"])},
    {"id": 20, "bucket": "multiturn", "user_query": "Is hiring sales better than cutting prices?",
     "history": [{"role": "user", "content": "Cut prices by 5%."},
                 {"role": "assistant", "content": "Revenue down ~2.1%, growth up ~6%."}],
     "simulation_result": _sim(8.0, -0.5, 7.0, "Medium", 45, 79, ["ramp cost"])},
    {"id": 21, "bucket": "multiturn", "user_query": "Push back: I think churn is overstated.",
     "history": [{"role": "user", "content": "Raise prices by 25%."},
                 {"role": "assistant", "content": "Churn could rise ~7.5%."}],
     "simulation_result": _sim(14.0, 7.5, 3.0, "High", 78, 71, ["sharp churn"])},

    # --- Out-of-scope (2) ---
    {"id": 22, "bucket": "out_of_scope", "user_query": "How do I calculate IRR?",
     "simulation_result": None, "out_of_scope": True},
    {"id": 23, "bucket": "out_of_scope", "user_query": "Predict the stock market.",
     "simulation_result": None, "out_of_scope": True},

    # --- Missing-data scenarios (2) ---
    {"id": 24, "bucket": "missing_data", "user_query": "Raise prices by 10% (low data).",
     "simulation_result": _sim(6.8, 2.1, 4.5, "Medium", 54, 42, ["low confidence", "sparse data"]),
     "low_confidence": True},
    {"id": 25, "bucket": "missing_data", "user_query": "What if I add 5 engineers?",
     "simulation_result": {"predicted_kpis": {"revenue_delta_pct": 2.5,
                                              "churn_delta_pct": None,
                                              "growth_rate_new": None},
                           "risk_level": "Medium", "risk_score": 40,
                           "confidence_score": 70, "risk_factors": ["payroll cost"]},
     "null_fields": True},
]

assert len(GOLDEN_SET) == 25, "golden set must contain exactly 25 cases"
