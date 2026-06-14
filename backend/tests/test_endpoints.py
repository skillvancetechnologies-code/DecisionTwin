"""Contract tests for all 8 REST endpoints: happy path + a negative case each."""
import pytest

from tests.conftest import SAMPLE_CSV

pytestmark = pytest.mark.asyncio


async def _upload(client) -> str:
    resp = await client.post(
        "/datasets/upload",
        files={"file": ("sales.csv", SAMPLE_CSV, "text/csv")},
        data={"dataset_name": "Q1 Sales", "file_type": "sales"},
    )
    assert resp.status_code == 200, resp.text
    return resp.json()["dataset_id"]


# 1. healthz
async def test_healthz(client):
    resp = await client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


# 2. upload (happy + negative)
async def test_upload_happy(client):
    resp = await client.post(
        "/datasets/upload",
        files={"file": ("sales.csv", SAMPLE_CSV, "text/csv")},
        data={"dataset_name": "Q1 Sales", "file_type": "sales"},
    )
    body = resp.json()
    assert resp.status_code == 200
    assert body["row_count"] == 4
    assert 0 <= body["quality_score"] <= 100
    assert any(c["name"] == "revenue" for c in body["columns"])


async def test_upload_negative_empty(client):
    resp = await client.post(
        "/datasets/upload",
        files={"file": ("empty.csv", "", "text/csv")},
        data={"dataset_name": "Empty", "file_type": "sales"},
    )
    assert resp.status_code == 400
    assert resp.json()["detail"]["error"] == "VALIDATION_FAILED"


# 3. preview (happy + negative)
async def test_preview_happy(client):
    ds = await _upload(client)
    resp = await client.get(f"/datasets/{ds}/preview")
    body = resp.json()
    assert resp.status_code == 200
    assert "revenue" in body["headers"]
    assert "revenue" in body["summary_stats"]


async def test_preview_negative_missing(client):
    resp = await client.get("/datasets/not-a-real-id/preview")
    assert resp.status_code == 404


# 4. baseline (happy + negative)
async def test_baseline_happy(client):
    ds = await _upload(client)
    resp = await client.get(f"/analytics/baseline/{ds}")
    body = resp.json()
    assert resp.status_code == 200
    assert "kpi_cards" in body["metrics"]


async def test_baseline_negative_missing(client):
    resp = await client.get("/analytics/baseline/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404


# 5. simulate (happy + negative)
async def test_simulate_happy(client):
    ds = await _upload(client)
    resp = await client.post(
        "/simulate",
        json={
            "dataset_id": ds,
            "decision_type": "price_change",
            "parameter": "price_per_unit",
            "magnitude": 10,
            "magnitude_type": "percentage",
        },
    )
    body = resp.json()
    assert resp.status_code == 200
    assert "predicted_kpis" in body
    assert 0 <= body["risk_score"] <= 100
    assert body["risk_level"] in {"Low", "Medium", "High"}


async def test_simulate_negative_bad_type(client):
    ds = await _upload(client)
    resp = await client.post(
        "/simulate",
        json={
            "dataset_id": ds,
            "decision_type": "invalid_type",
            "parameter": "x",
            "magnitude": 5,
            "magnitude_type": "percentage",
        },
    )
    assert resp.status_code == 422


# 6. chat (happy + negative)
async def test_chat_happy(client):
    resp = await client.post(
        "/chat",
        json={
            "user_session_id": "11111111-1111-1111-1111-111111111111",
            "user_message": "What if I raise prices by 10%?",
            "simulation_result": {
                "predicted_kpis": {"revenue_delta_pct": 6.8, "churn_delta_pct": 2.4},
                "risk_level": "Medium",
            },
        },
    )
    assert resp.status_code == 200
    text = resp.text
    assert "event: token" in text
    assert "event: done" in text


async def test_chat_negative_missing_field(client):
    resp = await client.post("/chat", json={"user_message": "hi"})
    assert resp.status_code == 422


# 7. scenarios save + compare (happy + negative)
async def _save(client, name: str, revenue_delta: float, risk: str, score: int) -> str:
    resp = await client.post(
        "/scenarios/save",
        json={
            "scenario_name": name,
            "user_query": "test",
            "simulation_result": {
                "predicted_kpis": {
                    "revenue_delta_pct": revenue_delta,
                    "growth_rate_new": revenue_delta + 5,
                    "churn_delta_pct": 1.0,
                },
                "risk_level": risk,
                "risk_score": score,
                "confidence_score": 80,
            },
        },
    )
    assert resp.status_code == 200, resp.text
    return resp.json()["scenario_id"]


async def test_save_and_compare_happy(client):
    a = await _save(client, "Price +10%", 6.8, "Medium", 54)
    b = await _save(client, "Hire 5", -1.2, "Low", 20)
    resp = await client.get(f"/scenarios/compare?ids={a},{b}")
    body = resp.json()
    assert resp.status_code == 200
    assert len(body["scenarios"]) == 2
    assert body["best_per_metric"]["revenue_delta_pct"] == a


async def test_save_negative_missing_field(client):
    resp = await client.post("/scenarios/save", json={"user_query": "x"})
    assert resp.status_code == 422


# 8. report (happy + negative)
async def test_report_happy(client):
    a = await _save(client, "Price +10%", 6.8, "Medium", 54)
    resp = await client.get(f"/scenarios/{a}/report")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/pdf"
    assert resp.content[:4] == b"%PDF"


async def test_report_negative_missing(client):
    resp = await client.get("/scenarios/00000000-0000-0000-0000-000000000000/report")
    assert resp.status_code == 404
