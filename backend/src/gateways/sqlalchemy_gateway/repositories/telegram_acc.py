from gateways.contracts import ITelegramAccountsRepo
from .base import SqlAlchemyRepository
from models import TelegramAccount


class TelegramAccountsRepo(SqlAlchemyRepository, ITelegramAccountsRepo):
    model = TelegramAccount

    async def get_by_user_id(self, user_id: int) -> TelegramAccount:
        return await super().get_one(user_id=user_id)

    async def get_by_id(self, acc_id: int) -> TelegramAccount:
        return await super().get_one(id=acc_id)

    async def delete_by_id(self, acc_id: int) -> None:
        return await super().delete_or_raise_not_found(id=acc_id)
