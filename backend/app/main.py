"""DecisionTwin FastAPI application entrypoint."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db import init_db
from app.routers import analytics, chat, datasets, health, scenarios, simulate


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup for local/dev (production relies on Alembic).
    await init_db()
    yield


app = FastAPI(
    title="DecisionTwin API",
    version="1.0.0",
    description="AI-powered decision-simulation copilot — application layer.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# All API endpoints live under /v1 (matches VITE_API_BASE_URL).
API_PREFIX = "/v1"
for r in (health, datasets, analytics, simulate, chat, scenarios):
    app.include_router(r.router, prefix=API_PREFIX)


@app.get("/")
def root():
    return {"service": "DecisionTwin API", "docs": "/docs", "version": "1.0.0"}
