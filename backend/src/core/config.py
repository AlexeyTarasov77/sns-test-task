import typing as t
from dotenv import load_dotenv

from pydantic import (
    BaseModel,
    Field,
    PostgresDsn,
)
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

PORT = t.Annotated[int, Field(gt=0, le=65535)]


class _Server(BaseModel):
    hostname: str = Field(default="0.0.0.0")
    port: PORT = Field(default=8000)


class Config(BaseSettings):
    model_config = SettingsConfigDict(extra="allow")
    server: _Server = Field(default=_Server())
    pg_dsn: PostgresDsn


load_dotenv()

app_config = Config()  # type: ignore
