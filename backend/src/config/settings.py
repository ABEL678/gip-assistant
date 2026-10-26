"""Настройки приложения. Загружаются из .env в корне репо."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Корень проекта: settings.py → config/ → src/ → backend/ → gip-assistant/
BASE_DIR = Path(__file__).resolve().parents[3]
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    """Все настройки ГИП-Ассистента."""

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # --- App ---
    APP_NAME: str = "GIP-Assistant"
    APP_ENV: str = "dev"
    APP_DEBUG: bool = True

    # --- Database ---
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "gip_assistant"
    DB_USER: str = "gip"
    DB_PASSWORD: str = "gip"

    # --- JWT ---
    JWT_SECRET: str = "change_me"
    JWT_ALG: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440

    # --- Telegram ---
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_DIGEST_CRON: str = "0 9 * * *"
    TELEGRAM_PROXY: str = ""

    # --- LLM ---
    LLM_ENCRYPTION_KEY: str = ""

    # --- CORS ---
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    # ---------- Computed ----------

    @property
    def database_url(self) -> str:
        """Async URL для SQLAlchemy (asyncpg)."""
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def sync_database_url(self) -> str:
        """Sync URL для Alembic / psycopg2."""
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    """Singleton-настройки."""
    return Settings()


settings = get_settings()
