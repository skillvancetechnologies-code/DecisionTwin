# DecisionTwin — Demo Runbook

## Start (local)

1. **Backend**: `cd backend && uvicorn app.main:app --reload --port 8000`
   (first run auto-creates the SQLite DB; Swagger at `/docs`).
2. **Frontend**: `cd frontend && npm run dev` → open http://localhost:5173.

## Demo script (~5 min, full happy path)

1. **Landing** → click **Get started**.
2. **Upload**: drop a sales CSV with `date,revenue,units_sold,region` columns,
   name it, pick `sales`, click **Upload & validate**. You see the quality
   score, warnings, and a preview table.
3. **Baseline**: click **View baseline** → 4 KPI cards + revenue trend line.
4. **Simulate**: click **Run a simulation**, keep "raise prices by 10%",
   **Run simulation** → result card with revenue/churn deltas, risk gauge,
   confidence band. Click **Save scenario**.
5. Repeat step 4 with a **headcount** and a **marketing** query, save each.
6. **Chat**: from a saved simulation click **Discuss in chat** → ask a question,
   watch the streamed (SSE) response.
7. **Dashboard**: see the saved scenarios, color-coded comparison table,
   timeline. Click **Download CSV** and **Download PDF**.

## Production smoke test (run against the deployed URL)

| # | Check |
|---|-------|
| 1 | `GET /v1/healthz` → 200 with build SHA |
| 2 | `POST /v1/datasets/upload` with sample CSV → `dataset_id` |
| 3 | `GET /v1/analytics/baseline/{id}` → `kpi_cards` |
| 4 | `POST /v1/simulate` (price_change) → `predicted_kpis` + `risk_score` |
| 5 | `POST /v1/chat` → streamed response |
| 6 | `POST /v1/scenarios/save` → `scenario_id` |
| 7 | `GET /v1/scenarios/{id}/report` → `application/pdf` |
| 8 | Frontend URL loads < 3s, all pages render |

## Restart / recovery

- Backend hangs: restart the Railway/Render service (or `Ctrl-C` + re-run uvicorn).
- DB migration needed: `alembic upgrade head`.
- Cache acting up: clear Redis or unset `REDIS_URL` to fall back to in-process cache.

## Environment variables

See `backend/.env.example` and `frontend/.env.example`.
