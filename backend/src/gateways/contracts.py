from abc import ABC, abstractmethod
from dto import SignUpDTO, TgAccountCredentialsDTO
from models import User
from datetime import timedelta

from models.user import TelegramAccount


class IUsersRepo(ABC):
    @abstractmethod
    async def get_by_username(self, username: str) -> User: ...
    @abstractmethod
    async def create(self, dto: SignUpDTO) -> User: ...


class ITelegramAccountsRepo(ABC):
    @abstractmethod
    async def create(self, acc: TelegramAccount) -> TelegramAccount: ...


class IPasswordHasher(ABC):
    @abstractmethod
    def compare(self, plain: str, hash: bytes) -> bool: ...


class IJwtTokenProvider(ABC):
    @abstractmethod
    def new_token(self, payload: dict, ttl: timedelta) -> str: ...


class ITelegramClient(ABC):
    def __init__(self, credentials: TgAccountCredentialsDTO, user_id: int):
        self._creds = credentials
        self._user_id = user_id

    @abstractmethod
    async def send_signin_code(self, phone_number: str) -> str: ...

    @abstractmethod
    async def confirm_signin_code(
        self,
        phone_number: str,
        phone_code_hash: str,
        code: str,
        password: str | None = None,
    ): ...


class ITelegramClientFactory:
    @abstractmethod
    def new_client(self, acc: TelegramAccount) -> ITelegramClient: ...
