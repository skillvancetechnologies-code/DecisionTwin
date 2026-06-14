from pydantic import BaseModel


class SimulationResult(BaseModel):

    revenue_change: float

    profit_change: float

    risk_score: float

    recommendation: str