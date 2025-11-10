"""Application configuration."""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Google Cloud Vision
    google_application_credentials: str = ""

    # Pokemon TCG API
    pokemon_tcg_api_key: str = ""
    pokemon_tcg_api_url: str = "https://api.pokemontcg.io/v2"

    # CORS - Allow both localhost and WSL IP for development
    cors_origins: str = "http://localhost:19006,http://localhost:8081,http://192.168.50.229:8081"

    # Timeouts (milliseconds)
    ocr_timeout_ms: int = 2500
    pricing_timeout_ms: int = 3000

    # Environment
    environment: str = "development"

    # Application
    app_name: str = "Pokemon Card Scanner API"
    app_version: str = "1.0.0"

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
