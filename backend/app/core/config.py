from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    APP_ENV: str = "development"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DATABASE_URL: str = "sqlite:///./infrastructure_monitoring.db"
    AI_PROVIDER: str = "nemotron"
    AI_MODEL: str = "<configured-nemotron-model>"
    AI_BASE_URL: str = ""
    AI_API_KEY: str = ""
    MAX_IMAGE_SIZE_MB: int = 10
    MAX_VIDEO_SIZE_MB: int = 100
    VIDEO_FRAME_SAMPLE_INTERVAL: int = 2

    class Config:
        env_file = ".env"


settings = Settings()