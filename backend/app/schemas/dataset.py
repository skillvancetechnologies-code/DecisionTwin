"""Schemas for dataset upload, preview, and baseline analytics."""
from typing import Any

from pydantic import BaseModel


class ColumnInfo(BaseModel):
    name: str
    dtype: str
    null_pct: float


class UploadResponse(BaseModel):
    dataset_id: str
    name: str
    columns: list[ColumnInfo]
    row_count: int
    quality_score: float
    warnings: list[str] = []


class PreviewResponse(BaseModel):
    headers: list[str]
    rows: list[list[Any]]
    summary_stats: dict[str, dict[str, float]]


class BaselineResponse(BaseModel):
    dataset_id: str
    metrics: dict[str, Any]
