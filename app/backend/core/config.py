"""Application configuration using Pydantic settings."""
from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Central application settings loaded from environment variables."""

    database_url: str = Field(
        "postgresql+psycopg2://myuser:paviliong6!@localhost:5433/mydatabase",
        env="DATABASE_URL",
    )
    redis_url: str = Field("redis://localhost:6379/0", env="REDIS_URL")
    public_base_url: str = Field("http://localhost:5434", env="PUBLIC_BASE_URL")
    label_printer: str = Field("MY_LABEL_PRINTER", env="LABEL_PRINTER")
    allowed_origins: List[str] = Field(
        default_factory=lambda: ["http://localhost:3000"], env="ALLOWED_ORIGINS"
    )
    media_dir: Path = Field(default=Path("./media"), env="MEDIA_DIR")

    class Config:
        env_file = Path(__file__).resolve().parents[2] / "ops" / ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Return cached settings instance."""

    settings = Settings()
    settings.media_dir.mkdir(parents=True, exist_ok=True)
    return settings
