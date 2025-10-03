"""Backend configuration settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Backend application settings."""

    # Database
    database_url: str

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # API Keys
    anthropic_api_key: str

    # Blockchain
    ethereum_rpc_url: str

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
