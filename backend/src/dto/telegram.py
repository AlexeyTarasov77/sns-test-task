from dto.base import BaseDTO
from datetime import datetime


class TgAccountCredentialsDTO(BaseDTO):
    api_id: int
    api_hash: str


class TgConnectRequestResultDTO(BaseDTO):
    phone_number: str
    phone_code_hash: str


class TgConnectRequestDTO(TgAccountCredentialsDTO):
    phone_number: str | None = None


class TgConnectConfirmDTO(TgConnectRequestDTO):
    password: str | None = None
    phone_code_hash: str
    phone_code: str


class BaseChatDTO(BaseDTO):
    id: int
    title: str
    photo_url: str | None = None


class TelegramChatDTO(BaseChatDTO):
    last_message: str | None = None


class TelegramAccountInfoDTO(BaseDTO):
    first_name: str | None = None
    last_name: str | None = None
    username: str | None
    photo_url: str | None = None
    display_name: str


class TelegramMessageDTO(BaseDTO):
    id: int
    date: datetime
    out: bool
    message: str
    reply_to_msg_id: int | None = None
    sender: TelegramAccountInfoDTO


class TelegramChatInfoDTO(BaseChatDTO):
    messages: list[TelegramMessageDTO]
