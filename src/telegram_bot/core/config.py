"""Telegram bot configuration."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Telegram bot settings."""

    # Telegram
    telegram_bot_token: str

    # Backend API
    backend_url: str = "http://localhost:8000"

    # AI
    anthropic_api_key: str

    # App
    debug: bool = False

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance.

    Returns:
        Settings instance
    """
    return Settings()
