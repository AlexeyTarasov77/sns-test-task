from sqlalchemy import func, select
from gateways.contracts import IUsersRepo
from gateways.exceptions import StorageNotFoundError
from models import User
from .base import SqlAlchemyRepository
from gateways.sqlalchemy_gateway import get_session


class UsersRepo(SqlAlchemyRepository, IUsersRepo):
    model = User

    async def get_by_username(self, username: str) -> User:
        stmt = select(self.model).where(
            func.lower(self.model.username) == func.lower(username)
        )
        async with get_session() as session:
            res = await session.execute(stmt)
        user = res.scalar_one_or_none()
        if not user:
            raise StorageNotFoundError()
        return user

    async def get_by_id(self, user_id: int) -> User:
        return await super().get_one(id=user_id)
