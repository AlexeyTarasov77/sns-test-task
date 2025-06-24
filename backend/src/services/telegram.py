from dto.telegram import TgAccountCredentialsDTO
from gateways.contracts import ITelegramAccountsRepo, ITelegramClientFactory
from gateways.exceptions import StorageAlreadyExistsError
from models import TelegramAccount
from services.exceptions import (
    InvalidTelegramAccCredentialsError,
    TelegramAccAlreadyConnectedError,
)


class TelegramService:
    def __init__(
        self,
        tg_client_factory: ITelegramClientFactory,
        tg_accounts_repo: ITelegramAccountsRepo,
    ):
        self._tg_client_factory = tg_client_factory
        self._tg_accounts_repo = tg_accounts_repo

    async def connect_tg(self, user_id: int, credentials: TgAccountCredentialsDTO):
        tg_acc = TelegramAccount(**credentials.model_dump(), user_id=user_id)
        tg_client = self._tg_client_factory.new_client(tg_acc)
        if not await tg_client.check_is_valid_creds():
            raise InvalidTelegramAccCredentialsError()
        try:
            return await self._tg_accounts_repo.create(tg_acc)
        except StorageAlreadyExistsError:
            raise TelegramAccAlreadyConnectedError()
