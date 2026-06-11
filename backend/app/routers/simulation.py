from fastapi import APIRouter
from app.schemas.simulation_schema import SimulationResult

router = APIRouter()


@router.get("/simulate/", response_model=SimulationResult)
def run_simulation():

    return SimulationResult(
        simulation_id=1,
        decision="Approved",
        revenue_delta=12.5,
        risk_level="Low",
        confidence_score=94.0
    )