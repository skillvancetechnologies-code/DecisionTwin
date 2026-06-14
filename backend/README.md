# DecisionTwin — Backend (FastAPI)

The application/API layer for DecisionTwin: CSV ingestion, baseline analytics,
decision simulation, streaming copilot chat, scenario save/compare, and PDF
reports. The ML and GenAI logic is consumed through thin adapters
(`app/integrations/`) so the real `dt_ml` / `dt_genai` packages drop in without
touching the routers.

## Quick start (local, zero infra)

```bash
cd backend
python -m venv .venv && source .venv/Scripts/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
# Swagger UI: http://localhost:8000/docs
```

Local dev defaults to **SQLite + an in-process cache**, so no Postgres/Redis is
required. Tables are created automatically on startup.

## With Postgres + Redis (Docker)

```bash
docker compose up --build
# Applies Alembic migrations, then serves on :8000
```

## Configuration

Copy `.env.example` to `.env`. All values are optional locally.

| Var | Purpose |
|-----|---------|
| `DATABASE_URL` | `postgresql+asyncpg://…` in prod; blank → SQLite |
| `REDIS_URL` | `redis://…`; blank → in-process cache |
| `OPENAI_API_KEY`, `GENAI_MODEL` | consumed by the GenAI module |
| `CORS_ORIGINS` | comma-separated allowed frontend origins |

## API (all under `/v1`)

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/v1/healthz` | health + build SHA |
| POST | `/v1/datasets/upload` | upload + validate CSV |
| GET | `/v1/datasets/{id}/preview` | first rows + summary stats |
| GET | `/v1/analytics/baseline/{id}` | baseline KPIs (cached 1h) |
| POST | `/v1/simulate` | run simulation (cached 10m) |
| POST | `/v1/chat` | streaming copilot (SSE) |
| POST | `/v1/scenarios/save` | save a scenario |
| GET | `/v1/scenarios/compare?ids=` | compare scenarios |
| GET | `/v1/scenarios/{id}/report` | PDF report |

## Migrations

```bash
alembic upgrade head                       # apply
alembic revision --autogenerate -m "msg"   # new migration
```

## Tests

```bash
pytest -q     # 15 contract tests, all 8 endpoints (happy + negative)
```
