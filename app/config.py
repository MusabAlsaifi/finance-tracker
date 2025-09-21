from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """App settings"""

    DATABASE_URL: str = "sqlite:///./finance_tracker.db"

    SECRET_KEY: str = "123"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 30

    APP_NAME: str = "Finance Tracker"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()