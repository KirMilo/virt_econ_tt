from pydantic import PostgresDsn, RedisDsn, field_validator
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

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


class RedisSettings(BaseSettings):
    host: str
    port: int
    url: str | None = None

    @field_validator("url", mode="before")
    def assemble_redis_connection(cls, v: str | None, values: ValidationInfo) -> str:  # NOQA
        if isinstance(v, str):
            return v
        return str(
            RedisDsn.build(
                scheme="redis",
                host=values.data.get("host"),
                port=values.data.get("port"),
            )
        )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False, env_nested_delimiter="__")

    api_v1_prefix: str = '/api/v1'

    db: DbSettings
    redis: RedisSettings


settings = Settings()  # NOQA
