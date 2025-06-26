from abc import ABC, abstractmethod
from typing import Any
from dto import TgAccountCredentialsDTO, TelegramChatDTO, TelegramChatInfoDTO
from models import User, TelegramAccount
from datetime import timedelta


class IUsersRepo(ABC):
    @abstractmethod
    async def get_by_username(self, username: str) -> User: ...
    @abstractmethod
    async def get_by_id(self, user_id: int) -> User: ...
    @abstractmethod
    async def save(self, instance: User) -> User: ...


class ITelegramAccountsRepo(ABC):
    @abstractmethod
    async def save(self, instance: TelegramAccount) -> TelegramAccount: ...

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> TelegramAccount: ...


class IPasswordHasher(ABC):
    @abstractmethod
    def compare(self, plain: str, hash: bytes) -> bool: ...

    @abstractmethod
    def hash(self, plain: str) -> bytes: ...


class IJwtTokenProvider(ABC):
    @abstractmethod
    def new_token(self, payload: dict, ttl: timedelta) -> str: ...

    @abstractmethod
    def extract_payload(self, token: str) -> dict[str, Any]: ...


class ITelegramClient(ABC):
    def __init__(self, acc: TelegramAccount):
        self._creds = TgAccountCredentialsDTO(api_id=acc.api_id, api_hash=acc.api_hash)
        self._user_id = acc.user_id
        self._phone_number = acc.phone_number

    @abstractmethod
    async def send_signin_code(self) -> str: ...

    @abstractmethod
    async def confirm_signin_code(
        self,
        phone_code_hash: str,
        phone_code: str,
        password: str | None = None,
    ): ...

    @abstractmethod
    async def get_all_chats(self) -> list[TelegramChatDTO]: ...

    @abstractmethod
    async def get_chat_by_id(self, chat_id: int) -> TelegramChatInfoDTO: ...


class ITelegramClientFactory:
    @abstractmethod
    def new_client(self, acc: TelegramAccount) -> ITelegramClient: ...
