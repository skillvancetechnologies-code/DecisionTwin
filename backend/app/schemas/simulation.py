"""Schemas for the /simulate endpoint."""
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class DecisionType(str, Enum):
    price_change = "price_change"
    headcount = "headcount"
    marketing = "marketing"


class MagnitudeType(str, Enum):
    percentage = "percentage"
    absolute = "absolute"


class SimulateRequest(BaseModel):
    dataset_id: str
    decision_type: DecisionType
    parameter: str = Field(..., examples=["price_per_unit"])
    magnitude: float = Field(..., examples=[10])
    magnitude_type: MagnitudeType = MagnitudeType.percentage


class PredictedKPIs(BaseModel):
    revenue_delta_pct: float
    revenue_delta_abs: float
    churn_delta_pct: float
    growth_rate_new: float


class SimulateResponse(BaseModel):
    simulation_id: str
    predicted_kpis: PredictedKPIs
    deltas: dict[str, dict[str, Any]]
    risk_level: str
    risk_score: int
    risk_factors: list[str]
    confidence_score: int
    model_used: str
