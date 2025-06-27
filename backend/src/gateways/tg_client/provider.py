import os
import asyncio
from telethon.hints import EntityLike
from telethon.tl.types import User as TgUser
from telethon.utils import get_display_name
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
    user: TgUser
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

    async def _download_photo(self, photo: EntityLike, filename: str) -> str:
        photo_path = app_root / app_config.media_path / filename
        if not photo_path.exists():
            await self._client.download_profile_photo(
                photo,
                photo_path.absolute().as_posix(),
            )
        photo_url = app_config.media_serve_url + "/" + filename
        return photo_url

    async def get_chat_by_id(self, chat_id: int) -> TelegramChatInfoDTO: ...

    async def get_all_chats(self) -> list[TelegramChatDTO]:
        res: list[TelegramChatDTO] = []
        async with self._client as client:
            async for chat in client.iter_dialogs():
                photo_url = None
                if chat.entity.photo:
                    filename = f"user_{self._user_id}_chat_{chat.entity.id}.jpg"
                    photo_url = await self._download_photo(chat.entity, filename)
                res.append(
                    TelegramChatDTO(
                        id=chat.entity.id,
                        title=get_display_name(chat.entity),
                        photo_url=photo_url,
                        last_message=chat.message.message,
                    )
                )
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
                photo_url = await self._download_photo(client.user, filename)
            return TelegramAccountInfoDTO.model_validate(
                {**client.user.to_dict(), "photo_url": photo_url}
            )

    async def delete_session(self) -> None:
        await asyncio.to_thread(os.remove, self._session_path)
