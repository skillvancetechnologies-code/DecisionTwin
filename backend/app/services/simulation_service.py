"""Simulation orchestration: ML engine + risk scorer with Redis caching."""
from __future__ import annotations

import hashlib
import json
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.cache import cache
from app.integrations.ml import run_simulation, score_risk
from app.schemas.simulation import SimulateRequest
from app.services.ingestion import _load_dataframe

SIMULATE_TTL = 600  # 10 minutes, per spec


def _request_hash(req: SimulateRequest) -> str:
    payload = req.model_dump(mode="json")
    blob = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(blob.encode()).hexdigest()[:16]


async def run(session: AsyncSession, req: SimulateRequest) -> dict:
    cache_key = f"simulate:{_request_hash(req)}"
    cached = await cache.get_json(cache_key)
    if cached is not None:
        return cached

    df = await _load_dataframe(session, req.dataset_id)
    prediction = run_simulation(
        df,
        decision_type=req.decision_type.value,
        parameter=req.parameter,
        magnitude=req.magnitude,
        magnitude_type=req.magnitude_type.value,
    )
    risk = score_risk(req.decision_type.value, req.magnitude, prediction)

    response = {
        "simulation_id": f"sim_{uuid.uuid4().hex[:12]}",
        "predicted_kpis": prediction["predicted_kpis"],
        "deltas": prediction["deltas"],
        "risk_level": risk["risk_level"],
        "risk_score": risk["risk_score"],
        "risk_factors": risk["risk_factors"],
        "confidence_score": prediction["confidence_score"],
        "model_used": prediction["model_used"],
    }
    await cache.set_json(cache_key, response, SIMULATE_TTL)
    return response
