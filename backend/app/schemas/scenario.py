"""Schemas for scenario save / compare."""
from typing import Any

from pydantic import BaseModel


class SaveScenarioRequest(BaseModel):
    scenario_name: str
    simulation_result: dict[str, Any]
    user_query: str
    ai_explanation: str | None = None
    dataset_id: str | None = None
    user_session_id: str | None = None


class SaveScenarioResponse(BaseModel):
    scenario_id: str
    saved_at: str


class ScenarioSummary(BaseModel):
    id: str
    name: str
    kpis: dict[str, Any]
    risk: str


class CompareResponse(BaseModel):
    scenarios: list[ScenarioSummary]
    comparison_table: list[dict[str, Any]]
    best_per_metric: dict[str, str]
