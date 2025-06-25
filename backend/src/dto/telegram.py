from dto.base import BaseDTO


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


class TelegramChatDTO(BaseDTO):
    id: int
    title: str
    photo_url: str
