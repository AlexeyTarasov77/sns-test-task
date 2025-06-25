from random import randint
from faker import Faker
from core.config import app_config

from dto.telegram import TgAccountCredentialsDTO
from gateways.exceptions import (
    TelegramInvalidCredentialsError,
    TelegramInvalidPhoneCodeError,
    TelegramInvalidPhoneNumberError,
)
from gateways.tg_client.provider import TelethonTgProvider
import pytest


@pytest.fixture
def telethon_provider() -> TelethonTgProvider | None:
    if not app_config.tg:
        return
    provider = TelethonTgProvider(
        TgAccountCredentialsDTO(
            api_id=app_config.tg.api_id, api_hash=app_config.tg.api_hash
        ),
        randint(1, 1000),
        "tg_sessions_test",
    )
    return provider


fake_phone_number = "380123456789"


@pytest.mark.asyncio
@pytest.mark.skipif(not app_config.tg, reason="requires tg credentials config to run")
class TestTelethonTgProvider:
    async def test_send_signin_code_success(
        self, telethon_provider: TelethonTgProvider
    ):
        assert app_config.tg is not None
        phone_hash_code = await telethon_provider.send_signin_code(
            app_config.tg.acc_phone
        )
        # check session was created
        assert telethon_provider._session_path.exists()
        assert phone_hash_code

    async def test_send_signin_code_invalid_creds(self, faker: Faker):
        assert app_config.tg is not None
        telethon_provider = TelethonTgProvider(
            TgAccountCredentialsDTO(api_id=12345, api_hash=faker.sha256()),
            randint(1, 1000),
            "tg_sessions_test",
        )
        with pytest.raises(TelegramInvalidCredentialsError):
            await telethon_provider.send_signin_code(app_config.tg.acc_phone)

    async def test_send_signin_code_invalid_phone(
        self, telethon_provider: TelethonTgProvider
    ):
        with pytest.raises(TelegramInvalidPhoneNumberError):
            await telethon_provider.send_signin_code(fake_phone_number)

    async def test_confirm_signin_code_invalid_code(
        self, telethon_provider: TelethonTgProvider, faker: Faker
    ):
        assert app_config.tg is not None
        with pytest.raises(TelegramInvalidPhoneCodeError):
            await telethon_provider.confirm_signin_code(
                app_config.tg.acc_phone,
                faker.sha256(),
                str(randint(10000, 99999)),
                faker.password(),
            )
