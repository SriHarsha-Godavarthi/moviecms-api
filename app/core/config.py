from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./movieflix.db"
    jwt_secret: str = "change_me_in_production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    # Environment controls
    environment: str = "development"  # e.g., development, staging, production
    auto_create_schema: bool = True    # disable in production to rely on Alembic

    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    return Settings()
