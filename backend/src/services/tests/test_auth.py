from datetime import timedelta
from random import randint
from typing import NamedTuple
from faker import Faker
from gateways.exceptions import StorageAlreadyExistsError, StorageNotFoundError
from models import User
from dto import SignInDTO, SignUpDTO
from gateways.contracts import IJwtTokenProvider, IPasswordHasher, IUsersRepo
import pytest
from services.auth import AuthService
from unittest.mock import Mock, create_autospec

from services.exceptions import (
    InvalidAuthCredentialsError,
    NotActiveUserError,
    UserAlreadyExistsError,
)


class AuthTestSuite(NamedTuple):
    service: AuthService
    mock_users_repo: Mock
    mock_password_hasher: Mock
    mock_jwt_provider: Mock


@pytest.fixture
def suite() -> AuthTestSuite:
    mock_users_repo = create_autospec(IUsersRepo)
    mock_password_hasher = create_autospec(IPasswordHasher)
    mock_jwt_provider = create_autospec(IJwtTokenProvider)
    service = AuthService(
        mock_users_repo, mock_password_hasher, mock_jwt_provider, timedelta(days=1)
    )
    return AuthTestSuite(
        service=service,
        mock_users_repo=mock_users_repo,
        mock_password_hasher=mock_password_hasher,
        mock_jwt_provider=mock_jwt_provider,
    )


@pytest.fixture
def fake_signin_dto(faker: Faker) -> SignInDTO:
    return SignInDTO(username=faker.user_name(), password=faker.password())


@pytest.fixture
def fake_signup_dto(faker: Faker) -> SignInDTO:
    return SignUpDTO(
        username=faker.user_name(),
        password=faker.password(),
        phone_number=faker.phone_number(),
    )


@pytest.mark.asyncio
class TestAuthService:
    async def test_signin_success(
        self, suite: AuthTestSuite, fake_signin_dto: SignInDTO, faker: Faker
    ):
        expected_user = User(
            id=randint(1, 100),
            phone_number=faker.phone_number(),
            username=fake_signin_dto.username,
            is_active=True,
            password_hash=fake_signin_dto.password.encode(),
        )
        expected_token = faker.password()
        suite.mock_jwt_provider.new_token.return_value = expected_token
        suite.mock_password_hasher.compare.return_value = True
        suite.mock_users_repo.get_by_username.return_value = expected_user
        res = await suite.service.signin(fake_signin_dto)
        suite.mock_users_repo.get_by_username.assert_awaited_once_with(
            fake_signin_dto.username
        )
        suite.mock_jwt_provider.new_token.assert_called_once_with(
            {"uid": expected_user.id}, suite.service._auth_token_ttl
        )
        suite.mock_password_hasher.compare.assert_called_once_with(
            fake_signin_dto.password, expected_user.password_hash
        )
        assert res.token == expected_token
        assert res.user.username == expected_user.username

    async def test_signin_not_found(
        self, suite: AuthTestSuite, fake_signin_dto: SignInDTO
    ):
        suite.mock_users_repo.get_by_username.side_effect = StorageNotFoundError()
        with pytest.raises(InvalidAuthCredentialsError):
            await suite.service.signin(fake_signin_dto)
        suite.mock_users_repo.get_by_username.assert_awaited_once_with(
            fake_signin_dto.username
        )

    async def test_signin_invalid_password(
        self, suite: AuthTestSuite, fake_signin_dto: SignInDTO
    ):
        expected_user = User(
            username=fake_signin_dto.username,
            is_active=True,
            password_hash=fake_signin_dto.password.encode(),
        )
        suite.mock_password_hasher.compare.return_value = False
        suite.mock_users_repo.get_by_username.return_value = expected_user
        with pytest.raises(InvalidAuthCredentialsError):
            await suite.service.signin(fake_signin_dto)
        suite.mock_users_repo.get_by_username.assert_awaited_once_with(
            fake_signin_dto.username
        )
        suite.mock_password_hasher.compare.assert_called_once_with(
            fake_signin_dto.password, expected_user.password_hash
        )

    async def test_signin_inactive_user(
        self, suite: AuthTestSuite, fake_signin_dto: SignInDTO
    ):
        expected_user = User(
            username=fake_signin_dto.username,
            is_active=False,
            password_hash=fake_signin_dto.password.encode(),
        )
        suite.mock_users_repo.get_by_username.return_value = expected_user
        with pytest.raises(NotActiveUserError):
            await suite.service.signin(fake_signin_dto)
        suite.mock_users_repo.get_by_username.assert_awaited_once_with(
            fake_signin_dto.username
        )

    async def test_signup_success(
        self, suite: AuthTestSuite, fake_signup_dto: SignUpDTO
    ):
        expected_hashed_password = fake_signup_dto.password.encode()
        expected_user = User(
            username=fake_signup_dto.username,
            phone_number=fake_signup_dto.phone_number,
            password_hash=expected_hashed_password,
        )
        suite.mock_password_hasher.hash.return_value = expected_hashed_password
        suite.mock_users_repo.save.return_value = expected_user
        user = await suite.service.signup(fake_signup_dto)
        suite.mock_users_repo.save.assert_awaited_once_with(expected_user)
        suite.mock_password_hasher.hash.assert_called_once_with(
            fake_signup_dto.password
        )
        assert user == expected_user

    async def test_signup_already_exists(
        self, suite: AuthTestSuite, fake_signup_dto: SignUpDTO
    ):
        expected_hashed_password = fake_signup_dto.password.encode()
        expected_user = User(
            username=fake_signup_dto.username,
            phone_number=fake_signup_dto.phone_number,
            password_hash=expected_hashed_password,
        )
        suite.mock_password_hasher.hash.return_value = expected_hashed_password
        suite.mock_users_repo.save.side_effect = StorageAlreadyExistsError()
        with pytest.raises(UserAlreadyExistsError):
            await suite.service.signup(fake_signup_dto)
        suite.mock_users_repo.save.assert_awaited_once_with(expected_user)
