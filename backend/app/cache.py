"""Redis cache wrapper with an in-process fallback.

When REDIS_URL is unset (local dev), an in-memory TTL dict is used so the
caching code paths behave identically without requiring a Redis server.
"""
import json
import time
from typing import Any

from app.config import settings

try:
    import redis.asyncio as aioredis
except ImportError:  # pragma: no cover
    aioredis = None


class _MemoryCache:
    def __init__(self) -> None:
        self._store: dict[str, tuple[float | None, str]] = {}

    async def get(self, key: str) -> str | None:
        item = self._store.get(key)
        if item is None:
            return None
        expires_at, value = item
        if expires_at is not None and expires_at < time.time():
            self._store.pop(key, None)
            return None
        return value

    async def set(self, key: str, value: str, ex: int | None = None) -> None:
        expires_at = time.time() + ex if ex else None
        self._store[key] = (expires_at, value)


class Cache:
    def __init__(self) -> None:
        if settings.redis_url and aioredis is not None:
            self._client: Any = aioredis.from_url(
                settings.redis_url, decode_responses=True
            )
            self.backend = "redis"
        else:
            self._client = _MemoryCache()
            self.backend = "memory"

    async def get_json(self, key: str) -> Any | None:
        raw = await self._client.get(key)
        return json.loads(raw) if raw is not None else None

    async def set_json(self, key: str, value: Any, ttl: int) -> None:
        await self._client.set(key, json.dumps(value, default=str), ex=ttl)


cache = Cache()
