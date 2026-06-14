def analyze_business_risk(user_query):

    query = user_query.lower()

    if any(word in query for word in [
        "hire",
        "hiring",
        "recruit",
        "employee",
        "attrition",
        "workforce"
    ]):
        category = "Human Resources"
        decision_type = "hr_change"
        risk = "Medium"
        probability = "40% - 60%"
        confidence = 0.85
        recommendation = (
            "Plan workforce expansion carefully and monitor productivity."
        )

    elif any(word in query for word in [
        "customer",
        "customers",
        "retention",
        "churn",
        "satisfaction",
        "loyalty",
        "complaint",
        "feedback"
    ]):
        category = "Customer"
        decision_type = "customer_change"
        risk = "Medium"
        probability = "50% - 70%"
        confidence = 0.88
        recommendation = (
            "Improve customer engagement and retention strategies."
        )

    elif any(word in query for word in [
        "revenue",
        "sales",
        "profit",
        "cost",
        "expenses",
        "budget"
    ]):
        category = "Finance"
        decision_type = "financial_change"
        risk = "High"
        probability = "70% - 90%"
        confidence = 0.92
        recommendation = (
            "Improve financial forecasting, optimize budgeting, and strengthen cost control measures."
        )

    else:
        category = "General"
        decision_type = "general"
        risk = "Low"
        probability = "20% - 40%"
        confidence = 0.70
        recommendation = (
            "Further business analysis is recommended."
        )

    return {
        "category": category,
        "decision_type": decision_type,
        "risk": risk,
        "probability": probability,
        "confidence": confidence,
        "recommendation": recommendation
    }