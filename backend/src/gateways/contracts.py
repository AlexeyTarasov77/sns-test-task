from abc import ABC, abstractmethod
from models import User
from datetime import timedelta


class IUsersRepo(ABC):
    @abstractmethod
    async def get_by_username(self, username: str) -> User: ...


class IPasswordHasher(ABC):
    @abstractmethod
    def compare(self, plain: str, hash: bytes) -> bool: ...


class IJwtTokenProvider(ABC):
    @abstractmethod
    def new_token(self, payload: dict, ttl: timedelta) -> str: ...
