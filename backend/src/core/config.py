from datetime import timedelta
from pathlib import Path
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


class Server(BaseModel):
    model_config = SettingsConfigDict(env_prefix="server_")
    hostname: str = Field(default="0.0.0.0")
    port: PORT = Field(default=8000)


class _Telegram(BaseModel):
    """Optional telegram credentials config.
    Credentials are used only in testing purposes"""

    model_config = SettingsConfigDict(env_prefix="tg_")
    api_id: int
    api_hash: str
    acc_phone: str


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__", extra="allow")
    server: Server = Field(default=Server())
    tg: _Telegram | None = None
    pg_dsn: PostgresDsn
    auth_token_ttl: timedelta = Field(default=timedelta(minutes=30))
    jwt_secret: str
    media_path: str = "media"

    @property
    def media_serve_url(self) -> str:
        return f"http://{self.server.hostname}:{self.server.port}/{self.media_path}"


load_dotenv()

app_config = Config()  # type: ignore
app_root = Path().parent
