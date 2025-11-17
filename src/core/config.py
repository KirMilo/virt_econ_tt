from pydantic import BaseModel
from pydantic_settings import BaseSettings


class DbSettings(BaseModel):
    url: str
    echo: bool = True


class CacheSettings(BaseModel):
    url: str


class Settings(BaseSettings):
    api_v1_prefix: str = '/api/v1'

    db: DbSettings = DbSettings()
    cache: CacheSettings = CacheSettings()
