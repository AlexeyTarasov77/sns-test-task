from random import randint
from faker import Faker
from core.config import app_config

from gateways.exceptions import (
    TelegramInvalidCredentialsError,
    TelegramInvalidPhoneCodeError,
    TelegramInvalidPhoneNumberError,
)
from gateways.tg_client.provider import TelethonTgProvider
import pytest

from models.user import TelegramAccount


def create_telethon_provider(
    phone_number: str, api_id: int | None = None, api_hash: str | None = None
) -> TelethonTgProvider:
    if not app_config.tg:
        return  # type: ignore
    provider = TelethonTgProvider(
        TelegramAccount(
            api_id=api_id or app_config.tg.api_id,
            api_hash=api_hash or app_config.tg.api_hash,
            user_id=randint(1, 1000),
            phone_number=phone_number,
        ),
        "tg_sessions_test",
    )
    return provider


fake_phone_number = "380123456789"


@pytest.mark.asyncio
@pytest.mark.skipif(not app_config.tg, reason="requires tg credentials config to run")
class TestTelethonTgProvider:
    async def test_send_signin_code_success(self):
        assert app_config.tg is not None
        telethon_provider = create_telethon_provider(app_config.tg.acc_phone)
        phone_hash_code = await telethon_provider.send_signin_code()
        # check session was created
        assert telethon_provider._session_path.exists()
        assert phone_hash_code

    async def test_send_signin_code_invalid_creds(self, faker: Faker):
        assert app_config.tg is not None
        telethon_provider = create_telethon_provider(
            app_config.tg.acc_phone, api_id=12345, api_hash=faker.sha256()
        )
        with pytest.raises(TelegramInvalidCredentialsError):
            await telethon_provider.send_signin_code()

    async def test_send_signin_code_invalid_phone(self):
        telethon_provider = create_telethon_provider(fake_phone_number)
        with pytest.raises(TelegramInvalidPhoneNumberError):
            await telethon_provider.send_signin_code()

    async def test_confirm_signin_code_invalid_code(self, faker: Faker):
        assert app_config.tg is not None
        telethon_provider = create_telethon_provider(app_config.tg.acc_phone)
        with pytest.raises(TelegramInvalidPhoneCodeError):
            await telethon_provider.confirm_signin_code(
                faker.sha256(),
                str(randint(10000, 99999)),
                faker.password(),
            )
