"""Application settings loaded from environment variables and `.env` files."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central runtime settings for storage and ingestion services."""

    environment: str = "dev"
    log_level: str = "INFO"

    postgres_db: str = "nowcast"
    postgres_user: str = "nowcast"
    postgres_password: str = "nowcast"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    database_url: str | None = None

    auto_create_tables: bool = True
    ingestion_source_timeout_seconds: int = Field(default=30, ge=1)

    @property
    def sqlalchemy_database_url(self) -> str:
        """Return the configured SQLAlchemy database URL.

        `DATABASE_URL` has priority. If it is not set, the URL is assembled
        from the individual PostgreSQL environment variables.
        """

        if self.database_url:
            return self.database_url

        return (
            "postgresql+psycopg://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""

    return Settings()
