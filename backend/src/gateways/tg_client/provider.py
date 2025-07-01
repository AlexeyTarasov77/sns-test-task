from collections.abc import AsyncGenerator
import os
import asyncio
from telethon.hints import EntityLike
from telethon.tl.types import Chat, User as TgUser
from telethon.utils import get_display_name
from core.config import app_root, app_config
from gateways.exceptions import (
    StorageNotFoundError,
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
from dto import (
    TelegramChatDTO,
    TelegramChatInfoDTO,
    TelegramAccountInfoDTO,
    TelegramMessageDTO,
)
from gateways.contracts import ITelegramClient
from models import TelegramAccount


class AuthOnlyTelethonClient(TelethonTelegramClient):
    """Overrides __aenter__ original method to avoid interactive login behaviour"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._active_users = 0
        self.auth_user: TgUser | None = None

    async def __aenter__(self):
        self._active_users += 1
        if not self.is_connected():
            await self.connect()

        # cache results to avoid calling every time
        if not self.auth_user:
            me = await self.get_me()
            if me is None:
                raise ValueError("Authentication failed. Unable to use client")
            self.auth_user = me  # type: ignore
        return self

    async def __aexit__(self, *args):
        self._active_users -= 1
        if self._active_users == 0:
            print("DISCONNECTING")
            await self.disconnect()  # type: ignore


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

    def _get_chat_avatar_filename(self, chat_id: int) -> str:
        return f"user_{self._user_id}_chat_{chat_id}.jpg"

    def _get_user_avatar_filename(self, user_id: int | None = None) -> str:
        return f"user_{user_id or self._user_id}_avatar.jpg"

    async def _download_photo(self, photo: EntityLike, filename: str) -> str:
        photo_path = app_root / app_config.media_path / filename
        if not photo_path.exists():
            await self._client.download_profile_photo(
                photo,
                photo_path.absolute().as_posix(),
            )
        photo_url = app_config.media_serve_url + "/" + filename
        return photo_url

    async def yield_all_messages(
        self, chat_id: int, chunk_size: int = 50, initial_offset_id: int = 0
    ) -> AsyncGenerator[list[TelegramMessageDTO], None]:
        offset_id = initial_offset_id
        async with self._client:
            while True:
                messages = await self._get_messages(chat_id, chunk_size, offset_id)
                if not messages:
                    break
                offset_id = messages[-1].id
                yield messages

    async def _get_messages(
        self, chat_id: int, limit: int, offset_id: int = 0
    ) -> list[TelegramMessageDTO]:
        """WARNING: This method should be called only after client is connected"""
        chat_messages: list[TelegramMessageDTO] = []
        async for msg in self._client.iter_messages(
            chat_id,
            limit,
            offset_id=offset_id,
        ):
            # skip non-text messages since it's not supported yet
            if not msg.message:
                continue
            photo_url = None
            if msg.sender.photo:
                filename = self._get_user_avatar_filename(msg.sender.id)
                photo_url = await self._download_photo(msg.sender, filename)
            chat_messages.append(
                TelegramMessageDTO.model_validate(
                    {
                        **msg.to_dict(),
                        "reply_to_msg_id": msg.reply_to.reply_to_msg_id
                        if msg.reply_to
                        else None,
                        "sender": {
                            **msg.sender.to_dict(),
                            "display_name": get_display_name(msg.sender),
                            "photo_url": photo_url,
                        },
                    }
                )
            )
        return chat_messages

    async def get_chat_by_id(
        self, chat_id: int, messages_limit: int = 10
    ) -> TelegramChatInfoDTO:
        async with self._client as client:
            try:
                chat: Chat | TgUser = await client.get_entity(chat_id)  # type: ignore
            except ValueError as e:
                raise StorageNotFoundError() from e
            photo_url = None
            if chat.photo:
                filename = (
                    self._get_chat_avatar_filename(chat.id)
                    if isinstance(chat, Chat)
                    else self._get_user_avatar_filename()
                )
                photo_url = await self._download_photo(chat, filename)
            chat_messages = await self._get_messages(chat.id, messages_limit)
            return TelegramChatInfoDTO(
                id=chat.id,
                title=get_display_name(chat),
                photo_url=photo_url,
                messages=chat_messages,
            )

    async def get_all_chats(self) -> list[TelegramChatDTO]:
        res: list[TelegramChatDTO] = []
        async with self._client as client:
            async for chat in client.iter_dialogs():
                photo_url = None
                if chat.entity.photo:
                    filename = self._get_chat_avatar_filename(chat.entity.id)
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
                password=password,  # type: ignore
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
            assert client.auth_user is not None
            if client.auth_user.photo:
                filename = self._get_user_avatar_filename()
                photo_url = await self._download_photo(client.auth_user, filename)
            return TelegramAccountInfoDTO.model_validate(
                {
                    **client.auth_user.to_dict(),
                    "display_name": get_display_name(client.auth_user),
                    "photo_url": photo_url,
                }
            )

    async def delete_session(self) -> None:
        await asyncio.to_thread(os.remove, self._session_path)
