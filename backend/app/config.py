"""Application settings loaded from environment / .env via pydantic-settings."""
import os
from functools import lru_cache

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_DATABASE_URL = "sqlite+aiosqlite:///./decisiontwin.db"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    app_env: str = "development"
    log_level: str = "INFO"

    # SQLite by default so the app runs locally with zero infra.
    # In production set DATABASE_URL to a postgresql+asyncpg://... URL.
    database_url: str = DEFAULT_DATABASE_URL

    # When empty, the cache layer falls back to an in-process dict.
    redis_url: str = ""

    # GenAI module config (consumed by the dt_genai package when installed).
    # dt_genai uses Mistral (open-mistral-7b) per the PM decision and reads
    # MISTRAL_API_KEY from the environment. Without a key it degrades to a
    # deterministic, LLM-free response so the app still runs locally.
    mistral_api_key: str = ""
    genai_model: str = "open-mistral-7b"

    # Comma-separated list of allowed CORS origins.
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    upload_dir: str = "uploads"

    @model_validator(mode="after")
    def _fill_blanks(self) -> "Settings":
        # Treat empty env values (e.g. DATABASE_URL=) as "use the default".
        if not self.database_url.strip():
            self.database_url = DEFAULT_DATABASE_URL
        # dt_genai reads MISTRAL_API_KEY straight from os.environ. When the key
        # only comes from backend/.env (via pydantic-settings), export it so the
        # GenAI package picks it up regardless of the process working directory.
        if self.mistral_api_key.strip():
            os.environ.setdefault("MISTRAL_API_KEY", self.mistral_api_key.strip())
        return self

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
