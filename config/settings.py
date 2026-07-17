from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "EcoTwin-FM"
    environment: str = "development"
    api_prefix: str = "/api"
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    database_url: str = "sqlite:///./ecotwin.db"
    openaq_api_key: str | None = None
    openaq_base_url: str = "https://api.openaq.org/v3"
    data_dir: Path = Path("data/raw")
    uci_air_quality_path: Path = Path("data/raw/uci_air_quality/AirQualityUCI.csv")
    weatherbench_path: Path = Path("data/raw/weatherbench")
    model_dir: Path = Path("models/saved")
    scheduler_enabled: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
