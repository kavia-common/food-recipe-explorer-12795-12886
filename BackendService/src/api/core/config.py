from functools import lru_cache
from pydantic import BaseSettings, Field
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    APP_NAME: str = Field(default="Food Recipe Explorer - BackendService", description="Application name")
    APP_VERSION: str = Field(default="1.0.0", description="Application version")
    ENV: str = Field(default="development", description="Environment (development|staging|production)")
    CORS_ALLOW_ORIGINS: List[str] = Field(
        default=["*"], description="Allowed CORS origins list"
    )

    # Placeholders for future integration
    DATABASE_URL: str | None = Field(default=None, description="Database URL (optional, not used in mock repo)")
    AUTH_ISSUER: str | None = Field(default=None, description="Auth issuer (OIDC) - placeholder")
    AUTH_AUDIENCE: str | None = Field(default=None, description="Auth audience - placeholder")
    AUTH_JWKS_URL: str | None = Field(default=None, description="JWKS URL - placeholder")
    SECRET_KEY: str = Field(default="dev-secret", description="Secret key for mock token signing (dev only)")

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
