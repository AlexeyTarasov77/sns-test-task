from core.config import app_root
from gateways.exceptions import (
    TelegramInvalidCredentialsError,
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
    ApiIdInvalidError,
)
from dto import TelegramChatDTO
from gateways.contracts import ITelegramClient
from models import TelegramAccount


class AuthOnlyTelethonClient(TelethonTelegramClient):
    """Overrides __aenter__ original method to avoid interactive login behaviour"""

    async def __aenter__(self):
        if not self.is_connected():
            await self.connect()

        me = await self.get_me()
        if me is None:
            raise ValueError("Authentication failed. Unable to use client")
        return self

    async def __aexit__(self, *args):
        print("\n\nEXITING\n\n", args)
        await self.disconnect()


class TelethonTgProvider(ITelegramClient):
    def __init__(
        self,
        acc: TelegramAccount,
        sessions_dirname: str = "tg_sessions",
    ):
        super().__init__(acc)
        sessions_dir = app_root / sessions_dirname
        if not sessions_dir.exists():
            sessions_dir.mkdir()
        self._session_path = sessions_dir / ("user_" + str(acc.user_id) + ".session")
        self._client = AuthOnlyTelethonClient(
            self._session_path, self._creds.api_id, self._creds.api_hash
        )

    async def get_all_chats(self) -> list[TelegramChatDTO]:
        async with self._client as client:
            print("AEXIT METHOD", client.__aexit__)
            res = [
                TelegramChatDTO.model_validate(chat)
                async for chat in client.iter_dialogs()
            ]
        return res

    async def send_signin_code(self) -> str:
        client = TelethonTelegramClient(
            self._session_path,
            self._creds.api_id,
            self._creds.api_hash,
        )
        await client.connect()
        try:
            sent_code = await client.sign_in(self._phone_number)
        except ApiIdInvalidError:
            raise TelegramInvalidCredentialsError()
        except BadRequestError:
            raise TelegramInvalidPhoneNumberError
        finally:
            await client.disconnect()  # type: ignore
        return sent_code.phone_code_hash  # type: ignore

    async def confirm_signin_code(
        self,
        phone_code_hash: str,
        phone_code: str,
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
                self._phone_number,
                phone_code,
                password=password,
                phone_code_hash=phone_code_hash,
            )
        except SessionPasswordNeededError:
            raise TelegramPasswordRequiredError()
        # for some reason PhoneCodeEmptyError is raised too, althoud code is not empty
        except (PhoneCodeInvalidError, PhoneCodeExpiredError, PhoneCodeEmptyError):
            raise TelegramInvalidPhoneCodeError()
        except ApiIdInvalidError:
            raise TelegramInvalidCredentialsError()
        except BadRequestError:
            raise TelegramInvalidPhoneNumberError
        finally:
            await client.disconnect()  # type: ignore
