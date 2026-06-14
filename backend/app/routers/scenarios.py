"""Scenario save, compare, and PDF report endpoints."""
from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import db_session
from app.schemas.scenario import (
    CompareResponse,
    SaveScenarioRequest,
    SaveScenarioResponse,
)
from app.services import scenarios_service

router = APIRouter(prefix="/scenarios", tags=["Scenarios"])


@router.post("/save", response_model=SaveScenarioResponse)
async def save(req: SaveScenarioRequest, session: AsyncSession = Depends(db_session)):
    scenario = await scenarios_service.save_scenario(session, req)
    return {
        "scenario_id": str(scenario.id),
        "saved_at": scenario.created_at.isoformat(),
    }


@router.get("/compare", response_model=CompareResponse)
async def compare(
    ids: str = Query(..., description="Comma-separated scenario ids"),
    session: AsyncSession = Depends(db_session),
):
    id_list = [i.strip() for i in ids.split(",") if i.strip()]
    scenarios = await scenarios_service.list_scenarios(session, id_list)
    return scenarios_service.build_comparison(scenarios)


@router.get("/{scenario_id}/report")
async def report(scenario_id: str, session: AsyncSession = Depends(db_session)):
    scenario = await scenarios_service.get_scenario(session, scenario_id)
    pdf_bytes = scenarios_service.render_pdf(scenario)
    filename = f"scenario_{scenario_id}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
