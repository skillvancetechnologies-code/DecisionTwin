from dt_genai.query_parser import parse
from dt_genai.classifier import classify_query
from dt_genai.simulator import simulate
from dt_genai.recommendation_generator import generate_recommendation
from dt_genai.history_store import save_decision
from dt_genai.scoring import calculate_score
from dt_genai.report_generator import generate_report
from dt_genai.ml_connector import predict_business_outcome


def process_query(user_query: str):

    parsed = parse(user_query)

    route = classify_query(parsed)

    prediction = predict_business_outcome(
        parsed
    )

    simulation = simulate(parsed)

    recommendation = generate_recommendation(
        parsed,
        simulation
    )

    decision_score = calculate_score(
        simulation
    )

    result = {

        "user_query": user_query,

        "parsed_query": parsed.model_dump(),

        "ml_route": route,

        "ml_prediction": prediction,

        "simulation_result": simulation.model_dump(),

        "decision_score": decision_score,

        "ai_recommendation": recommendation
    }

    decision_report = generate_report(
        result
    )

    result["decision_report"] = decision_report

    save_decision(result)

    return result