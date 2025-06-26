from functools import lru_cache
import typing as t
from fastapi import Depends
import punq

from core.config import app_config
from gateways.contracts import (
    IJwtTokenProvider,
    IPasswordHasher,
    ITelegramAccountsRepo,
    ITelegramClientFactory,
    IUsersRepo,
)
from gateways.tg_client.factory import TelethonTgClientFactory
from gateways.security.tokens import JwtTokenProvider
from gateways.sqlalchemy_gateway.repositories import UsersRepo, TelegramAccountsRepo
from gateways.security.hashing import BcryptHasher
from services.auth import AuthService
from services.telegram import TelegramService


@lru_cache(1)
def get_container() -> punq.Container:
    return init_container()


def init_container() -> punq.Container:
    container = punq.Container()
    container.register(IUsersRepo, UsersRepo)
    container.register(ITelegramAccountsRepo, TelegramAccountsRepo)
    container.register(IPasswordHasher, BcryptHasher)
    container.register(
        IJwtTokenProvider, JwtTokenProvider, secret_key=app_config.jwt_secret
    )
    container.register(ITelegramClientFactory, TelethonTgClientFactory)
    container.register(
        AuthService, AuthService, auth_token_ttl=app_config.auth_token_ttl
    )
    container.register(TelegramService)

    return container


def Resolve[T](dep: type[T] | str, **kwargs) -> T:
    return t.cast(T, get_container().resolve(dep, **kwargs))


def Inject[T](dep: type[T] | str, **kwargs):
    def resolver() -> T:
        return Resolve(dep, **kwargs)

    return Depends(resolver)
