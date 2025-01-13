from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    debug: bool = False

    model_config = SettingsConfigDict(
        env_prefix="KV_",
        env_file=".env",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
