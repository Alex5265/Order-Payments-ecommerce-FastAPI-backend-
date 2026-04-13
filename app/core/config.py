from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    # App
    app_name : str = "App FastAPI ecommerce"
    debug: bool = False
    environment: Literal["development", "testing", "production"] = "development"
    secret_key: str = "supper_pupper_insecure_default_key"

    # Database
    postgres_user: str = "PostgresUsername"
    postgres_password: str = "password"
    postgres_db: str = "fastapi_db"
    db_host: str = "localhost"
    db_port: int = 5432
    db_debug: bool = True

    # more if need. give name



    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.db_host}:{self.db_port}/{self.postgres_db}"


@lru_cache
def get_settings() -> Settings:
    return Settings()

