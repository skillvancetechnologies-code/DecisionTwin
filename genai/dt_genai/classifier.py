from .schemas import ParsedQuery


def classify_query(query: ParsedQuery):

    if query.decision_type == "price_change":
        return "pricing_model"

    elif query.decision_type == "headcount":
        return "workforce_model"

    elif query.decision_type == "marketing":
        return "marketing_model"

    return "general_model"