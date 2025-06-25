from faker import Faker
from dto import TgConnectRequestDTO
from uuid import uuid4
from gateways.contracts import (
    ITelegramAccountsRepo,
    ITelegramClient,
    ITelegramClientFactory,
    IUsersRepo,
)
from random import randint
from gateways.exceptions import (
    TelegramInvalidCredentialsError,
    TelegramInvalidPhoneNumberError,
)
from models.user import TelegramAccount, User
import pytest
from typing import NamedTuple
from unittest.mock import Mock, create_autospec

from services.exceptions import (
    InvalidTelegramAccCredentialsError,
    TelegramAccNotExistError,
)
from services.telegram import TelegramService


class TelegramTestSuite(NamedTuple):
    service: TelegramService
    mock_tg_factory: Mock
    mock_tg_client: Mock
    mock_tg_acc_repo: Mock
    mock_users_repo: Mock


@pytest.fixture
def suite() -> TelegramTestSuite:
    mock_tg_factory = create_autospec(ITelegramClientFactory)
    mock_tg_client = create_autospec(ITelegramClient)
    mock_tg_factory.new_client.return_value = mock_tg_client
    mock_tg_acc_repo = create_autospec(ITelegramAccountsRepo)
    mock_users_repo = create_autospec(IUsersRepo)
    service = TelegramService(mock_tg_factory, mock_tg_acc_repo, mock_users_repo)
    return TelegramTestSuite(
        service=service,
        mock_tg_factory=mock_tg_factory,
        mock_tg_client=mock_tg_client,
        mock_tg_acc_repo=mock_tg_acc_repo,
        mock_users_repo=mock_users_repo,
    )


@pytest.fixture
def fake_connect_dto(faker: Faker):
    return TgConnectRequestDTO(
        api_id=randint(10000, 100000),
        api_hash=str(uuid4()),
        phone_number=faker.phone_number(),
    )


@pytest.mark.asyncio
class TestTelegramService:
    async def test_request_tg_connect_success(
        self,
        suite: TelegramTestSuite,
        fake_connect_dto: TgConnectRequestDTO,
        faker: Faker,
    ):
        test_user = User(id=randint(1, 100), phone_number=faker.phone_number())
        expected_phone_code_hash = faker.sha256()
        suite.mock_tg_client.send_signin_code.return_value = expected_phone_code_hash
        suite.mock_users_repo.get_by_id.return_value = test_user
        res = await suite.service.request_tg_connect(test_user.id, fake_connect_dto)
        assert res.phone_number == fake_connect_dto.phone_number
        assert res.phone_code_hash == expected_phone_code_hash
        suite.mock_tg_client.send_signin_code.assert_awaited_once()
        suite.mock_users_repo.get_by_id.assert_awaited_once_with(test_user.id)
        suite.mock_tg_factory.new_client.assert_called_with(
            TelegramAccount(
                user_id=test_user.id,
                phone_number=fake_connect_dto.phone_number,
                api_id=fake_connect_dto.api_id,
                api_hash=fake_connect_dto.api_hash,
            )
        )

    async def test_request_tg_connect_invalid_creds(
        self, suite: TelegramTestSuite, fake_connect_dto: TgConnectRequestDTO
    ):
        test_user_id = randint(1, 100)
        suite.mock_tg_client.send_signin_code.side_effect = (
            TelegramInvalidCredentialsError()
        )
        with pytest.raises(InvalidTelegramAccCredentialsError):
            await suite.service.request_tg_connect(test_user_id, fake_connect_dto)

    async def test_request_tg_connect_invalid_phone(
        self, suite: TelegramTestSuite, fake_connect_dto: TgConnectRequestDTO
    ):
        test_user_id = randint(1, 100)
        suite.mock_tg_client.send_signin_code.side_effect = (
            TelegramInvalidPhoneNumberError()
        )
        with pytest.raises(TelegramAccNotExistError):
            await suite.service.request_tg_connect(test_user_id, fake_connect_dto)
