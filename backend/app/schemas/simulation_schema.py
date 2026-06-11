from pydantic import BaseModel


class SimulationResult(BaseModel):
    simulation_id: int
    decision: str
    revenue_delta: float
    risk_level: str
    confidence_score: float