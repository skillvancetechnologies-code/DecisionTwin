"""Baseline analytics endpoint (Redis-cached for 1 hour)."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import db_session
from app.schemas.dataset import BaselineResponse
from app.services import ingestion

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/baseline/{dataset_id}", response_model=BaselineResponse)
async def baseline(dataset_id: str, session: AsyncSession = Depends(db_session)):
    return await ingestion.get_baseline(session, dataset_id)
