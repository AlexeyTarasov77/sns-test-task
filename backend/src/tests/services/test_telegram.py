from dto.telegram import TgAccountCredentialsDTO
from uuid import uuid4
from gateways.contracts import (
    ITelegramAccountsRepo,
    ITelegramClient,
    ITelegramClientFactory,
)
from random import randint
from gateways.exceptions import StorageAlreadyExistsError
from models.user import TelegramAccount
import pytest
from typing import NamedTuple
from unittest.mock import Mock, create_autospec

from services.exceptions import (
    InvalidTelegramAccCredentialsError,
    TelegramAccAlreadyConnectedError,
)
from services.telegram import TelegramService


class TelegramTestSuite(NamedTuple):
    service: TelegramService
    mock_tg_factory: Mock
    mock_tg_client: Mock
    mock_tg_acc_repo: Mock


@pytest.fixture
def suite() -> TelegramTestSuite:
    mock_tg_factory = create_autospec(ITelegramClientFactory)
    mock_tg_client = create_autospec(ITelegramClient)
    mock_tg_factory.new_client.return_value = mock_tg_client
    mock_tg_acc_repo = create_autospec(ITelegramAccountsRepo)
    service = TelegramService(mock_tg_factory, mock_tg_acc_repo)
    return TelegramTestSuite(
        service=service,
        mock_tg_factory=mock_tg_factory,
        mock_tg_client=mock_tg_client,
        mock_tg_acc_repo=mock_tg_acc_repo,
    )


@pytest.fixture
def fake_creds_dto():
    return TgAccountCredentialsDTO(api_id=randint(10000, 100000), api_hash=str(uuid4()))


@pytest.mark.asyncio
class TestTelegramService:
    async def test_connect_tg_success(
        self, suite: TelegramTestSuite, fake_creds_dto: TgAccountCredentialsDTO
    ):
        test_user_id = randint(1, 100)
        expected_tg_acc = TelegramAccount()
        suite.mock_tg_client.check_is_valid_creds.return_value = True
        suite.mock_tg_acc_repo.create.return_value = expected_tg_acc
        tg_acc = await suite.service.connect_tg(
            test_user_id, credentials=fake_creds_dto
        )
        suite.mock_tg_client.check_is_valid_creds.assert_awaited_once()
        suite.mock_tg_acc_repo.create.assert_awaited_once()
        assert tg_acc == expected_tg_acc

    async def test_connect_tg_invalid_creds(
        self, suite: TelegramTestSuite, fake_creds_dto: TgAccountCredentialsDTO
    ):
        test_user_id = randint(1, 100)
        suite.mock_tg_client.check_is_valid_creds.return_value = False
        with pytest.raises(InvalidTelegramAccCredentialsError):
            await suite.service.connect_tg(test_user_id, credentials=fake_creds_dto)
        suite.mock_tg_client.check_is_valid_creds.assert_awaited_once()

    async def test_connect_tg_already_connected(
        self, suite: TelegramTestSuite, fake_creds_dto: TgAccountCredentialsDTO
    ):
        test_user_id = randint(1, 100)
        suite.mock_tg_client.check_is_valid_creds.return_value = True
        suite.mock_tg_acc_repo.create.side_effect = StorageAlreadyExistsError
        with pytest.raises(TelegramAccAlreadyConnectedError):
            await suite.service.connect_tg(test_user_id, credentials=fake_creds_dto)
        suite.mock_tg_client.check_is_valid_creds.assert_awaited_once()
        suite.mock_tg_acc_repo.create.assert_awaited_once()
