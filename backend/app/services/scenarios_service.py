"""Scenario save, comparison, and PDF report services."""
from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import NotFound
from app.integrations.genai import build_pdf
from app.models.scenario import Scenario
from app.schemas.scenario import SaveScenarioRequest

# Whether a higher value is better for each comparable metric.
COLOR_DIRECTION = {
    "revenue_delta_pct": "higher_is_better",
    "growth_rate_new": "higher_is_better",
    "churn_delta_pct": "lower_is_better",
    "risk_score": "lower_is_better",
    "confidence_score": "higher_is_better",
}

METRIC_LABELS = {
    "revenue_delta_pct": "Revenue Delta %",
    "growth_rate_new": "New Growth Rate",
    "churn_delta_pct": "Churn Delta %",
    "risk_score": "Risk Score",
    "confidence_score": "Confidence",
}


def _coerce(value: str | None) -> uuid.UUID:
    try:
        return uuid.UUID(value) if value else uuid.uuid4()
    except (ValueError, TypeError):
        return uuid.uuid4()


async def save_scenario(session: AsyncSession, req: SaveScenarioRequest) -> Scenario:
    result = req.simulation_result or {}
    scenario = Scenario(
        user_session_id=_coerce(req.user_session_id),
        dataset_id=_coerce(req.dataset_id) if req.dataset_id else None,
        name=req.scenario_name,
        user_query=req.user_query,
        decision_type=result.get("decision_type", "price_change"),
        parameters=result.get("parameters", {}),
        result=result,
        ai_explanation=req.ai_explanation,
    )
    session.add(scenario)
    await session.commit()
    await session.refresh(scenario)
    return scenario


async def list_scenarios(session: AsyncSession, ids: list[str]) -> list[Scenario]:
    uuids = []
    for i in ids:
        try:
            uuids.append(uuid.UUID(i))
        except (ValueError, TypeError):
            continue
    rows = (
        await session.execute(select(Scenario).where(Scenario.id.in_(uuids)))
    ).scalars().all()
    by_id = {str(s.id): s for s in rows}
    return [by_id[i] for i in ids if i in by_id]


def _metric_value(scenario: Scenario, key: str) -> float | None:
    result = scenario.result or {}
    kpis = result.get("predicted_kpis", {})
    if key in kpis:
        return kpis[key]
    if key in result:
        return result[key]
    return None


def build_comparison(scenarios: list[Scenario]) -> dict:
    summaries = [
        {
            "id": str(s.id),
            "name": s.name,
            "kpis": (s.result or {}).get("predicted_kpis", {}),
            "risk": (s.result or {}).get("risk_level", "Unknown"),
        }
        for s in scenarios
    ]

    table: list[dict] = []
    best_per_metric: dict[str, str] = {}
    for key, direction in COLOR_DIRECTION.items():
        values = {str(s.id): _metric_value(s, key) for s in scenarios}
        present = {k: v for k, v in values.items() if v is not None}
        if not present:
            continue
        higher = direction == "higher_is_better"
        ordered = sorted(present.items(), key=lambda kv: kv[1], reverse=higher)
        best_id, worst_id = ordered[0][0], ordered[-1][0]
        row = {"metric": METRIC_LABELS[key], "best": best_id, "worst": worst_id}
        row.update(values)
        table.append(row)
        best_per_metric[key] = best_id

    return {
        "scenarios": summaries,
        "comparison_table": table,
        "best_per_metric": best_per_metric,
    }


async def get_scenario(session: AsyncSession, scenario_id: str) -> Scenario:
    try:
        sid = uuid.UUID(scenario_id)
    except (ValueError, TypeError):
        raise NotFound("Scenario")
    scenario = await session.get(Scenario, sid)
    if scenario is None:
        raise NotFound("Scenario")
    return scenario


def render_pdf(scenario: Scenario) -> bytes:
    return build_pdf(
        {
            "name": scenario.name,
            "user_query": scenario.user_query,
            "decision_type": scenario.decision_type,
            "result": scenario.result,
            "ai_explanation": scenario.ai_explanation,
        }
    )
