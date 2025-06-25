from dto import (
    TgConnectConfirmDTO,
    TgConnectRequestDTO,
    TgConnectRequestResultDTO,
    TelegramChatDTO,
)
from gateways.contracts import ITelegramAccountsRepo, ITelegramClientFactory, IUsersRepo
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
    ) -> TelegramAccount:
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
            return await self._tg_accounts_repo.create(tg_acc)
        except StorageAlreadyExistsError:
            raise TelegramAccAlreadyConnectedError()

    async def list_chats(self, user_id: int) -> list[TelegramChatDTO]:
        try:
            tg_acc = await self._tg_accounts_repo.get_by_user_id(user_id)
        except StorageNotFoundError:
            raise TelegramAccNotConnectedError()
        tg_client = self._tg_client_factory.new_client(tg_acc)
        return await tg_client.get_all_chats()
