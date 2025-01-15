from functools import lru_cache

from pydantic import PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # API
    debug: bool = False

    max_page_size: PositiveInt = 50

    # DB
    pg_user: str
    pg_pass: str
    pg_db: str = "kovoc"

    model_config = SettingsConfigDict(
        env_prefix="KV_",
        env_file=".env",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
