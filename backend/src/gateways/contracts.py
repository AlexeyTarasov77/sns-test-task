from abc import ABC, abstractmethod
from dto import SignUpDTO
from models import User
from datetime import timedelta


class IUsersRepo(ABC):
    @abstractmethod
    @abstractmethod
    async def get_by_username(self, username: str) -> User: ...
    async def create(self, dto: SignUpDTO) -> User: ...


class IPasswordHasher(ABC):
    @abstractmethod
    def compare(self, plain: str, hash: bytes) -> bool: ...


class IJwtTokenProvider(ABC):
    @abstractmethod
    def new_token(self, payload: dict, ttl: timedelta) -> str: ...
