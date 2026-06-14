from dt_genai.schemas_simulation import SimulationResult


def simulate(parsed_query):

    magnitude = abs(parsed_query.magnitude)

    if parsed_query.decision_type == "price_change":

        return SimulationResult(
            revenue_change=magnitude * 1.5,
            profit_change=magnitude * 1.2,
            risk_score=min(magnitude / 100, 1.0),
            recommendation="Price change simulation completed."
        )

    if parsed_query.decision_type == "marketing":

        return SimulationResult(
            revenue_change=magnitude * 1.2,
            profit_change=magnitude * 0.8,
            risk_score=min(magnitude / 120, 1.0),
            recommendation="Marketing simulation completed."
        )

    if parsed_query.decision_type == "headcount":

        return SimulationResult(
            revenue_change=magnitude * 0.5,
            profit_change=-(magnitude * 0.3),
            risk_score=min(magnitude / 50, 1.0),
            recommendation="Headcount simulation completed."
        )

    return SimulationResult(
        revenue_change=0.0,
        profit_change=0.0,
        risk_score=0.1,
        recommendation="No simulation available."
    ) 
