"""Pytest fixtures: isolated in-memory DB + async test client."""
import asyncio
import os

import pytest
import pytest_asyncio

# Force an isolated SQLite DB and in-memory cache before app import.
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test_decisiontwin.db"
os.environ["REDIS_URL"] = ""

import httpx  # noqa: E402
from httpx import ASGITransport  # noqa: E402

from app.db import engine, init_db  # noqa: E402
from app.main import app  # noqa: E402
from app.models.base import Base  # noqa: E402


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def _setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await init_db()
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://test/v1"
    ) as ac:
        yield ac


SAMPLE_CSV = (
    "date,revenue,units_sold,region\n"
    "2024-01-01,45200,901,North\n"
    "2024-02-01,47800,940,North\n"
    "2024-03-01,51200,1010,South\n"
    "2024-04-01,49900,980,South\n"
)
