from fastapi import APIRouter
from app.services.ml_service import get_baseline_metrics

router = APIRouter()


@router.get("/analytics")
def analytics():

    metrics = get_baseline_metrics()

    return {
        "status": "success",
        "result": metrics
    }