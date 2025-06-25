from core.config import app_root
from gateways.exceptions import (
    TelegramInvalidPhoneCodeError,
    TelegramInvalidPhoneNumberError,
    TelegramPasswordRequiredError,
)
from telethon import TelegramClient as TelethonTelegramClient
from telethon.errors import (
    SessionPasswordNeededError,
    BadRequestError,
    PhoneCodeExpiredError,
    PhoneCodeInvalidError,
    PhoneCodeEmptyError,
)
from gateways.contracts import ITelegramClient
from dto import TgAccountCredentialsDTO


class AuthOnlyTelethonClient(TelethonTelegramClient):
    """Overrides __aenter__ original method to avoid interactive login behaviour"""

    async def __aenter__(self):
        if not self.is_connected():
            await self.connect()

        me = await self.get_me()
        if me is None:
            raise ValueError("Authentication failed. Unable to use client")


class TelethonTgProvider(ITelegramClient):
    def __init__(
        self,
        credentials: TgAccountCredentialsDTO,
        user_id: int,
        sessions_dirname: str = "tg_sessions",
    ):
        super().__init__(credentials, user_id)
        sessions_dir = app_root / sessions_dirname
        if not sessions_dir.exists():
            sessions_dir.mkdir()
        self._session_path = sessions_dir / ("user_" + str(user_id) + ".session")
        self._client = AuthOnlyTelethonClient(
            self._session_path, self._creds.api_id, self._creds.api_hash
        )

    async def get_chats(self): ...

    async def send_signin_code(self, phone_number: str) -> str:
        client = TelethonTelegramClient(
            self._session_path,
            self._creds.api_id,
            self._creds.api_hash,
        )
        await client.connect()
        try:
            sent_code = await client.sign_in(phone_number)
        except BadRequestError:
            raise TelegramInvalidPhoneNumberError
        finally:
            await client.disconnect()  # type: ignore
        return sent_code.phone_code_hash  # type: ignore

    async def confirm_signin_code(
        self,
        phone_number: str,
        phone_code_hash: str,
        code: str,
        password: str | None = None,
    ):
        client = TelethonTelegramClient(
            self._session_path,
            self._creds.api_id,
            self._creds.api_hash,
        )
        await client.connect()
        try:
            await client.sign_in(
                phone_number, code, password=password, phone_code_hash=phone_code_hash
            )
        except SessionPasswordNeededError:
            raise TelegramPasswordRequiredError()
        # for some reason PhoneCodeEmptyError is raised too, althoud code is not empty
        except (PhoneCodeInvalidError, PhoneCodeExpiredError, PhoneCodeEmptyError):
            raise TelegramInvalidPhoneCodeError()
        except BadRequestError:
            raise TelegramInvalidPhoneNumberError
        finally:
            await client.disconnect()  # type: ignore
