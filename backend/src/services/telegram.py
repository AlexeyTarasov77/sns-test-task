from dto import (
    TgConnectConfirmDTO,
    TgConnectRequestDTO,
    TgConnectRequestResultDTO,
    TelegramChatDTO,
    TelegramChatInfoDTO,
    UserTelegramAccDTO,
    TelegramAccountInfoDTO,
)
from gateways.contracts import (
    ITelegramAccountsRepo,
    ITelegramClientFactory,
    ITelegramMessagesReader,
    IUsersRepo,
)
from gateways.exceptions import (
    StorageAlreadyExistsError,
    StorageNotFoundError,
    TelegramInvalidCredentialsError,
    TelegramInvalidPhoneCodeError,
    TelegramInvalidPhoneNumberError,
    TelegramPasswordRequiredError,
)
from models import TelegramAccount
from services.exceptions import (
    ChatNotFoundError,
    InvalidConfirmationCodeError,
    InvalidTelegramAccCredentialsError,
    TelegramAcc2FARequired,
    TelegramAccAlreadyConnectedError,
    TelegramAccNotConnectedError,
    TelegramAccNotExistError,
)


class TelegramService:
    def __init__(
        self,
        tg_client_factory: ITelegramClientFactory,
        tg_accounts_repo: ITelegramAccountsRepo,
        users_repo: IUsersRepo,
    ):
        self._tg_client_factory = tg_client_factory
        self._tg_accounts_repo = tg_accounts_repo
        self._users_repo = users_repo

    async def request_tg_connect(
        self, user_id: int, dto: TgConnectRequestDTO
    ) -> TgConnectRequestResultDTO:
        user = await self._users_repo.get_by_id(user_id)
        phone_number = dto.phone_number or user.phone_number
        tg_acc = TelegramAccount(
            user_id=user_id,
            api_id=dto.api_id,
            api_hash=dto.api_hash,
            phone_number=phone_number,
        )
        tg_client = self._tg_client_factory.new_client(tg_acc)
        try:
            phone_code_hash = await tg_client.send_signin_code()
        except TelegramInvalidCredentialsError:
            raise InvalidTelegramAccCredentialsError()
        except TelegramInvalidPhoneNumberError:
            raise TelegramAccNotExistError()
        return TgConnectRequestResultDTO(
            phone_number=phone_number, phone_code_hash=phone_code_hash
        )

    async def confirm_tg_connect(
        self, user_id: int, dto: TgConnectConfirmDTO
    ) -> UserTelegramAccDTO:
        tg_acc = TelegramAccount(
            user_id=user_id,
            api_id=dto.api_id,
            api_hash=dto.api_hash,
            phone_number=dto.phone_number,
        )

        tg_client = self._tg_client_factory.new_client(tg_acc)
        try:
            await tg_client.confirm_signin_code(
                dto.phone_code_hash,
                dto.phone_code,
                dto.password,
            )
        except TelegramPasswordRequiredError as e:
            raise TelegramAcc2FARequired from e
        except TelegramInvalidPhoneCodeError as e:
            raise InvalidConfirmationCodeError from e
        except TelegramInvalidCredentialsError as e:
            raise InvalidTelegramAccCredentialsError() from e
        except TelegramInvalidPhoneNumberError as e:
            raise TelegramAccNotExistError() from e
        try:
            tg_acc = await self._tg_accounts_repo.save(tg_acc)
        except StorageAlreadyExistsError:
            raise TelegramAccAlreadyConnectedError()
        acc_info = await self.get_account_info(tg_acc.id)
        return UserTelegramAccDTO(
            id=tg_acc.id,
            api_id=tg_acc.api_id,
            phone_number=tg_acc.phone_number,
            created_at=tg_acc.created_at,
            info=TelegramAccountInfoDTO.model_validate(acc_info),
        )

    async def list_chats(self, user_id: int) -> list[TelegramChatDTO]:
        try:
            tg_acc = await self._tg_accounts_repo.get_by_user_id(user_id)
        except StorageNotFoundError:
            raise TelegramAccNotConnectedError()
        tg_client = self._tg_client_factory.new_client(tg_acc)
        return await tg_client.get_all_chats()

    async def get_chat(
        self, user_id: int, chat_id: int, messages_limit: int = 10
    ) -> tuple[TelegramChatInfoDTO, ITelegramMessagesReader]:
        try:
            tg_acc = await self._tg_accounts_repo.get_by_user_id(user_id)
        except StorageNotFoundError:
            raise TelegramAccNotConnectedError()
        tg_client = self._tg_client_factory.new_client(tg_acc)
        try:
            chat = await tg_client.get_chat_by_id(chat_id, messages_limit)
        except StorageNotFoundError:
            raise ChatNotFoundError()
        return chat, tg_client

    async def get_account_info(self, acc_id: int):
        try:
            tg_acc = await self._tg_accounts_repo.get_by_id(acc_id)
        except StorageNotFoundError:
            raise TelegramAccNotConnectedError()
        tg_client = self._tg_client_factory.new_client(tg_acc)
        return await tg_client.get_me()

    async def remove_tg_acc(self, user_id: int):
        try:
            tg_acc = await self._tg_accounts_repo.get_by_user_id(user_id)
        except StorageNotFoundError:
            raise TelegramAccNotConnectedError()
        await self._tg_accounts_repo.delete_by_id(tg_acc.id)
        tg_client = self._tg_client_factory.new_client(tg_acc)
        await tg_client.delete_session()
