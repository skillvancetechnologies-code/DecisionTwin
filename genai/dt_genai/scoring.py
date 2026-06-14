def calculate_score(simulation_result):

    score = (
        simulation_result.revenue_change * 0.4
        + simulation_result.profit_change * 0.4
        - simulation_result.risk_score * 10 * 0.2
    )

    return round(score, 2)