from dt_genai.history_store import get_history


def get_dashboard():

    history = get_history()

    if not history:

        return {
            "total_decisions": 0,
            "average_score": 0,
            "best_decision": None,
            "worst_decision": None
        }

    scores = [
        item["decision_score"]
        for item in history
    ]

    best = max(
        history,
        key=lambda x: x["decision_score"]
    )

    worst = min(
        history,
        key=lambda x: x["decision_score"]
    )

    return {

        "total_decisions": len(history),

        "average_score": round(
            sum(scores) / len(scores),
            2
        ),

        "best_decision": best["user_query"],

        "worst_decision": worst["user_query"]
    }