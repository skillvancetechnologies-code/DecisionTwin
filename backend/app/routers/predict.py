from fastapi import APIRouter
from pydantic import BaseModel
from app.services.ml_service import predict_fraud

router = APIRouter()


class Transaction(BaseModel):
    V1: float
    V2: float
    V3: float
    Amount: float


@router.post("/predict")
def predict(transaction: Transaction):

    data = transaction.dict()

    result = predict_fraud(data)

    return {
        "status": "success",
        "result": result
    }