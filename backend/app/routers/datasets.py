"""Dataset upload and preview endpoints."""
from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import db_session
from app.schemas.dataset import PreviewResponse, UploadResponse
from app.services import ingestion

router = APIRouter(prefix="/datasets", tags=["Datasets"])


@router.post("/upload", response_model=UploadResponse)
async def upload_dataset(
    file: UploadFile = File(...),
    dataset_name: str = Form(...),
    file_type: str = Form("sales"),
    user_session_id: str | None = Form(None),
    session: AsyncSession = Depends(db_session),
):
    raw = await file.read()
    return await ingestion.ingest_csv(
        session,
        raw=raw,
        dataset_name=dataset_name,
        file_type=file_type,
        user_session_id=user_session_id,
    )


@router.get("/{dataset_id}/preview", response_model=PreviewResponse)
async def preview_dataset(
    dataset_id: str, session: AsyncSession = Depends(db_session)
):
    return await ingestion.get_preview(session, dataset_id)
