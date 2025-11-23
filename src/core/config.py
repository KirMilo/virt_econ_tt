from pydantic import PostgresDsn, field_validator, BaseModel
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
from os import environ

load_dotenv()


class DbSettings(BaseSettings):
    host: str
    port: int
    user: str
    password: str
    name: str
    url: str | None = None

    @field_validator("url", mode="before")
    def assemble_db_connection(cls, v: str | None, values: ValidationInfo) -> str:  # NOQA
        if isinstance(v, str):
            return v
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=values.data.get("user"),
                password=values.data.get("password"),
                host=values.data.get("host"),
                port=values.data.get("port"),
                path=values.data.get("name"),
            )
        )


class RedisSettings(BaseModel):
    host: str = environ.get("REDIS__HOST")
    port: int = int(environ.get("REDIS__PORT"))
    db: int = int(environ.get("REDIS__DB", 0))


class CacheNamespace(BaseModel):
    user_inventory: str = "user_inventory"
    analytics: str = "analytics"
    idempotency_key: str = "idempotency_key"


class CacheSettings(BaseModel):
    prefix: str = "fastapi-cache"
    namespace: CacheNamespace = CacheNamespace()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False, env_nested_delimiter="__")

    db: DbSettings
    redis: RedisSettings = RedisSettings()
    cache: CacheSettings = CacheSettings()

settings = Settings()  # NOQA
