"""Application settings loaded from environment / .env via pydantic-settings."""
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
    openai_api_key: str = ""
    genai_model: str = "gpt-4o-mini"

    # Comma-separated list of allowed CORS origins.
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    upload_dir: str = "uploads"

    @model_validator(mode="after")
    def _fill_blanks(self) -> "Settings":
        # Treat empty env values (e.g. DATABASE_URL=) as "use the default".
        if not self.database_url.strip():
            self.database_url = DEFAULT_DATABASE_URL
        return self

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
