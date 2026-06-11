import pandas as pd
import os
import joblib

# Load trained model
model = joblib.load("fraud_model.pkl")


def load_dataset():
    file_path = "uploads/creditcard.csv"

    if not os.path.exists(file_path):
        return None

    return pd.read_csv(file_path)


# =========================
# Week 3 Analytics Function
# =========================
def get_baseline_metrics():
    df = load_dataset()

    if df is None:
        return {"error": "Dataset not found"}

    total_transactions = len(df)
    fraud_cases = len(df[df["Class"] == 1])
    normal_cases = len(df[df["Class"] == 0])

    fraud_percentage = round(
        (fraud_cases / total_transactions) * 100,
        2
    )

    return {
        "total_transactions": total_transactions,
        "fraud_cases": fraud_cases,
        "normal_cases": normal_cases,
        "fraud_percentage": fraud_percentage
    }


# =========================
# Week 4 Prediction Function
# =========================
def predict_fraud(data: dict):

    print("\n========== REQUEST RECEIVED ==========")
    print(data)

    sample = {
        "Time": 0,
        "V1": 0,
        "V2": 0,
        "V3": 0,
        "V4": 0,
        "V5": 0,
        "V6": 0,
        "V7": 0,
        "V8": 0,
        "V9": 0,
        "V10": 0,
        "V11": 0,
        "V12": 0,
        "V13": 0,
        "V14": 0,
        "V15": 0,
        "V16": 0,
        "V17": 0,
        "V18": 0,
        "V19": 0,
        "V20": 0,
        "V21": 0,
        "V22": 0,
        "V23": 0,
        "V24": 0,
        "V25": 0,
        "V26": 0,
        "V27": 0,
        "V28": 0,
        "Amount": 0
    }

    sample.update(data)

    df = pd.DataFrame([sample])

    print("\n========== MODEL INPUT ==========")
    print(df.head())

    print("\n========== COLUMNS ==========")
    print(df.columns.tolist())

    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0].max()

    print("\n========== RESULT ==========")
    print("Prediction:", prediction)
    print("Confidence:", probability)

    return {
        "prediction": int(prediction),
        "confidence": round(float(probability) * 100, 2)
    }