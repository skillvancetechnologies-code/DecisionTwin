from fastapi import APIRouter
from app.routers.datasets import dataset_store
import pandas as pd

router = APIRouter()

@router.get("/datasets/{dataset_id}/statistics")
def dataset_statistics(dataset_id: int):

    if dataset_id not in dataset_store:
        return {"error": "Dataset not found"}

    file_path = dataset_store[dataset_id]

    df = pd.read_csv(file_path)

    fraud_count = 0
    normal_count = 0

    if "Class" in df.columns:
        fraud_count = int((df["Class"] == 1).sum())
        normal_count = int((df["Class"] == 0).sum())

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": int(df.isnull().sum().sum()),
        "fraud_records": fraud_count,
        "normal_records": normal_count
    }