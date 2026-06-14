"""Simulation endpoint."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import db_session
from app.schemas.simulation import SimulateRequest, SimulateResponse
from app.services import simulation_service

router = APIRouter(tags=["Simulate"])


@router.post("/simulate", response_model=SimulateResponse)
async def simulate(
    req: SimulateRequest, session: AsyncSession = Depends(db_session)
):
    return await simulation_service.run(session, req)
