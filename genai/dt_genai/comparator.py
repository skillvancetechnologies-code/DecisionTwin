from dt_genai.pipeline import process_query


def compare_scenarios(query_a, query_b):

    result_a = process_query(query_a)

    result_b = process_query(query_b)

    score_a = result_a["decision_score"]

    score_b = result_b["decision_score"]

    if score_a > score_b:

        best = "scenario_a"

        explanation = (
            "Scenario A provides the higher business score."
        )

    elif score_b > score_a:

        best = "scenario_b"

        explanation = (
            "Scenario B provides the higher business score."
        )

    else:

        best = "tie"

        explanation = (
            "Both scenarios perform similarly."
        )

    return {

        "scenario_a": result_a,

        "scenario_b": result_b,

        "best_scenario": best,

        "comparison_explanation": explanation
    }