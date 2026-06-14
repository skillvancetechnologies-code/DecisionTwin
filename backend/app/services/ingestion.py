"""Dataset ingestion, preview, and baseline analytics services."""
from __future__ import annotations

import uuid

import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache import cache
from app.core.csv_validator import parse_and_validate
from app.core.errors import NotFound
from app.integrations.ml import compute_baseline
from app.models.dataset import BaselineResult, Dataset, DatasetRow

BASELINE_TTL = 3600  # 1 hour, per spec


async def ingest_csv(
    session: AsyncSession,
    *,
    raw: bytes,
    dataset_name: str,
    file_type: str,
    user_session_id: str | None,
) -> dict:
    parsed = parse_and_validate(raw)
    session_uuid = _coerce_session(user_session_id)

    dataset = Dataset(
        user_session_id=session_uuid,
        name=dataset_name,
        file_type=file_type,
        columns=parsed["columns"],
        row_count=parsed["row_count"],
        quality_score=parsed["quality_score"],
    )
    session.add(dataset)
    await session.flush()  # populate dataset.id

    session.add_all(
        DatasetRow(dataset_id=dataset.id, row_index=i, payload=row)
        for i, row in enumerate(parsed["rows"])
    )
    await session.commit()

    return {
        "dataset_id": str(dataset.id),
        "name": dataset.name,
        "columns": parsed["columns"],
        "row_count": parsed["row_count"],
        "quality_score": parsed["quality_score"],
        "warnings": parsed["warnings"],
    }


async def _load_dataframe(session: AsyncSession, dataset_id: str) -> pd.DataFrame:
    ds = await _get_dataset(session, dataset_id)
    rows = (
        await session.execute(
            select(DatasetRow)
            .where(DatasetRow.dataset_id == ds.id)
            .order_by(DatasetRow.row_index)
        )
    ).scalars().all()
    df = pd.DataFrame([r.payload for r in rows])
    # Re-coerce date-like columns serialized to strings in JSON.
    from app.core.csv_validator import _is_textual

    for col in df.columns:
        if _is_textual(df[col]):
            coerced = pd.to_datetime(df[col], errors="coerce", format="mixed")
            if coerced.notna().mean() > 0.8:
                df[col] = coerced
    return df


async def get_preview(session: AsyncSession, dataset_id: str) -> dict:
    df = await _load_dataframe(session, dataset_id)
    headers = [str(c) for c in df.columns]
    head = df.head(5).where(pd.notna(df.head(5)), None)
    rows = head.astype(object).values.tolist()

    summary_stats: dict[str, dict[str, float]] = {}
    for col in df.select_dtypes("number").columns:
        s = df[col].dropna()
        if not s.empty:
            summary_stats[str(col)] = {
                "min": round(float(s.min()), 2),
                "max": round(float(s.max()), 2),
                "mean": round(float(s.mean()), 2),
                "stddev": round(float(s.std(ddof=0)), 2),
            }
    return {"headers": headers, "rows": rows, "summary_stats": summary_stats}


async def get_baseline(session: AsyncSession, dataset_id: str) -> dict:
    cache_key = f"baseline:{dataset_id}"
    cached = await cache.get_json(cache_key)
    if cached is not None:
        return cached

    ds = await _get_dataset(session, dataset_id)
    df = await _load_dataframe(session, dataset_id)
    metrics = compute_baseline(df)

    existing = await session.get(BaselineResult, ds.id)
    if existing is None:
        session.add(BaselineResult(dataset_id=ds.id, metrics=metrics))
    else:
        existing.metrics = metrics
    await session.commit()

    payload = {"dataset_id": dataset_id, "metrics": metrics}
    await cache.set_json(cache_key, payload, BASELINE_TTL)
    return payload


async def _get_dataset(session: AsyncSession, dataset_id: str) -> Dataset:
    try:
        ds_uuid = uuid.UUID(dataset_id)
    except (ValueError, TypeError):
        raise NotFound("Dataset")
    ds = await session.get(Dataset, ds_uuid)
    if ds is None:
        raise NotFound("Dataset")
    return ds


def _coerce_session(value: str | None) -> uuid.UUID:
    if not value:
        return uuid.uuid4()
    try:
        return uuid.UUID(value)
    except (ValueError, TypeError):
        return uuid.uuid4()
