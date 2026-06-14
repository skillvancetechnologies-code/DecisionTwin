def predict_business_outcome(parsed_query):

    if parsed_query.decision_type == "price_change":

        return {
            "predicted_revenue_change": 15.0,
            "predicted_profit_change": 12.0,
            "predicted_risk_score": 0.1,
            "model_confidence": 0.90
        }

    elif parsed_query.decision_type == "marketing":

        return {
            "predicted_revenue_change": 30.0,
            "predicted_profit_change": 20.0,
            "predicted_risk_score": 0.2,
            "model_confidence": 0.88
        }

    elif parsed_query.decision_type == "headcount":

        return {
            "predicted_revenue_change": 2.5,
            "predicted_profit_change": -1.5,
            "predicted_risk_score": 0.1,
            "model_confidence": 0.85
        }

    return {
        "predicted_revenue_change": 0.0,
        "predicted_profit_change": 0.0,
        "predicted_risk_score": 0.5,
        "model_confidence": 0.5
    }