def generate_recommendation(
    parsed_query,
    simulation_result
):

    if simulation_result.profit_change > 0:

        return (
            "The decision shows positive business impact. "
            "Proceed while monitoring key business metrics."
        )

    elif simulation_result.profit_change < 0:

        return (
            "The decision may negatively impact profitability. "
            "Further analysis is recommended before implementation."
        )

    return (
        "Business impact appears neutral. "
        "Review additional factors before proceeding."
    )