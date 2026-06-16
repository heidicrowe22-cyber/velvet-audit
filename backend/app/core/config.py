"""Application configuration."""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    APP_NAME: str = "Velvet Hour Audit"
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"
    SECRET_KEY: str = "change-this-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./velvethour.db"

    # Redis (optional, for background tasks)
    REDIS_URL: Optional[str] = None

    # Stripe
    STRIPE_SECRET_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    # Scan defaults
    SCAN_TIMEOUT_SECONDS: int = 120
    MAX_SCAN_PAGES: int = 5

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()