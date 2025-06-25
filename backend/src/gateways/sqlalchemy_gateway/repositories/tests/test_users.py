import pytest
from gateways.contracts import IUsersRepo
from models import User
from gateways.sqlalchemy_gateway.repositories import UsersRepo


@pytest.fixture
def users_repo() -> IUsersRepo:
    return UsersRepo()


@pytest.mark.asyncio
class TestUsersRepo:
    async def test_get_by_id_success(self, users_repo: IUsersRepo, test_user: User):
        found_user = await users_repo.get_by_id(test_user.id)
        assert found_user == test_user

    async def test_get_by_username_success(
        self, users_repo: IUsersRepo, test_user: User
    ):
        found_user = await users_repo.get_by_username(test_user.username)
        assert found_user == test_user

    async def test_save_success(self, users_repo: IUsersRepo, fake_user_data: dict):
        created_user = await users_repo.save(User(**fake_user_data))
        user_from_db = await users_repo.get_by_username(created_user.username)
        assert created_user == user_from_db
