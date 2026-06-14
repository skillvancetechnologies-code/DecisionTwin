# DecisionTwin

An AI-powered **decision-simulation copilot**. Upload your company CSV (sales,
HR, marketing), ask a natural-language question like *"What if I raise prices by
10%?"*, and DecisionTwin runs an ML simulation, scores the risk, explains the
result in plain English, and lets you save and compare scenarios on a visual
dashboard.

```
┌──────────────┐   HTTPS/JSON   ┌─────────────────┐   imports   ┌──────────────┐
│ React (Vite) │ ─────────────► │ FastAPI (/v1)   │ ──────────► │ dt_ml / dt_  │
│  + Tailwind  │ ◄───────────── │ Postgres + Redis│             │ genai (stub) │
└──────────────┘   SSE stream   └─────────────────┘             └──────────────┘
```

## Repository layout

| Path | What |
|------|------|
| `backend/` | FastAPI app — 8 REST endpoints, SQLAlchemy 2.0, Alembic, Redis cache, tests, Docker. See [backend/README.md](backend/README.md). |
| `frontend/` | React 19 + Vite + Tailwind SPA — 7 pages, charts, streaming chat, CSV/PDF export. See [frontend/README.md](frontend/README.md). |
| `.github/workflows/` | CI for backend (pytest) and frontend (lint + build). |

## Run it locally (two terminals)

**Backend** (defaults to SQLite + in-memory cache, no infra needed):
```bash
cd backend
python -m venv .venv && source .venv/Scripts/activate   # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
# http://localhost:8000/docs
```

**Frontend**:
```bash
cd frontend
npm install
cp .env.example .env.local         # VITE_API_BASE_URL=http://localhost:8000/v1
npm run dev
# http://localhost:5173
```

For Postgres + Redis instead of SQLite: `cd backend && docker compose up --build`.

## The 8 endpoints (all under `/v1`)

`GET /healthz` · `POST /datasets/upload` · `GET /datasets/{id}/preview` ·
`GET /analytics/baseline/{id}` · `POST /simulate` · `POST /chat` (SSE) ·
`POST /scenarios/save` · `GET /scenarios/compare` · `GET /scenarios/{id}/report` (PDF)

## ML / GenAI integration

The ML and GenAI teams ship `dt_ml` and `dt_genai` as pip packages. The web
backend consumes them through thin adapters in `backend/app/integrations/`. When
those packages are not installed, the adapters fall back to reference
implementations that compute real values from the uploaded data — so the full
product runs today, and the real modules drop in without touching any routers.

## Deployment

- **Frontend → Vercel**: set `VITE_API_BASE_URL` to the backend URL; SPA
  rewrites are in `frontend/vercel.json`.
- **Backend → Railway / Render**: set `DATABASE_URL`, `REDIS_URL`, `CORS_ORIGINS`;
  `backend/Procfile` runs migrations then uvicorn.

See [docs/RUNBOOK.md](docs/RUNBOOK.md) for the demo-day checklist.
