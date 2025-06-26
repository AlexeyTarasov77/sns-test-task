from time import time
from telethon.tl.types import User
from core.config import app_root, app_config
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
from dto import TelegramChatDTO, TelegramChatInfoDTO, TelegramAccountInfoDTO
from gateways.contracts import ITelegramClient
from models import TelegramAccount


class AuthOnlyTelethonClient(TelethonTelegramClient):
    user: User
    """Overrides __aenter__ original method to avoid interactive login behaviour"""

    async def __aenter__(self):
        if not self.is_connected():
            await self.connect()

        me = await self.get_me()
        if me is None:
            raise ValueError("Authentication failed. Unable to use client")
        self.user = me  # type: ignore
        return self

    async def __aexit__(self, *args):
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

    async def get_chat_by_id(self, chat_id: int) -> TelegramChatInfoDTO: ...

    async def get_all_chats(self) -> list[TelegramChatDTO]:
        # TODO: add fetching last message for every chat
        async with self._client as client:
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

    async def get_me(self) -> TelegramAccountInfoDTO:
        async with self._client as client:
            photo_url = None
            if client.user.photo:
                filename = f"user_{self._user_id}_avatar.jpg"
                photo_path = app_root / app_config.media_path / filename
                if not photo_path.exists():
                    await client.download_profile_photo(
                        client.user,
                        photo_path.absolute().as_posix(),
                    )
                photo_url = app_config.media_serve_url + "/" + filename
            return TelegramAccountInfoDTO.model_validate(
                {**client.user.to_dict(), "photo_url": photo_url}
            )
