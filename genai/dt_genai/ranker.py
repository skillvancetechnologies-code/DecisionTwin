from dt_genai.pipeline import process_query


def rank_decisions(queries):

    results = []

    for query in queries:

        result = process_query(query)

        results.append(result)

    ranked = sorted(
        results,
        key=lambda x: x["decision_score"],
        reverse=True
    )

    return ranked