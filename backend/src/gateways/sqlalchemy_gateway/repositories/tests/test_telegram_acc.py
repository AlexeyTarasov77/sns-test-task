from faker import Faker
from random import randint
import pytest
import pytest_asyncio
from sqlalchemy import delete
from gateways.contracts import ITelegramAccountsRepo
from gateways.sqlalchemy_gateway.repositories.telegram_acc import TelegramAccountsRepo
from models import TelegramAccount, User
from gateways.sqlalchemy_gateway import get_session


@pytest.fixture
def tg_repo() -> ITelegramAccountsRepo:
    return TelegramAccountsRepo()


@pytest.fixture()
def fake_acc_data(faker: Faker):
    return {
        "api_id": randint(10000, 99999),
        "api_hash": faker.sha256(),
        "phone_number": faker.phone_number(),
    }


@pytest_asyncio.fixture
async def test_acc(fake_acc_data: dict, test_user: User):
    acc = TelegramAccount(**fake_acc_data, user_id=test_user.id)

    async with get_session() as session:
        session.add(acc)
    yield acc
    async with get_session() as session:
        await session.execute(delete(TelegramAccount).filter_by(id=acc.id))


@pytest.mark.asyncio
class TestTelegramAccountsRepo:
    async def test_get_by_user_id_success(
        self, tg_repo: ITelegramAccountsRepo, test_acc: TelegramAccount
    ):
        found_acc = await tg_repo.get_by_user_id(test_acc.user_id)
        assert found_acc == test_acc

    async def test_save_success(
        self, tg_repo: ITelegramAccountsRepo, fake_acc_data: dict, test_user: User
    ):
        created_acc = await tg_repo.save(
            TelegramAccount(**fake_acc_data, user_id=test_user.id)
        )
        acc_from_db = await tg_repo.get_by_user_id(created_acc.user_id)
        assert created_acc == acc_from_db
