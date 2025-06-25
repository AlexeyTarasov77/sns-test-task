import pytest_asyncio
import pytest
from faker import Faker
from sqlalchemy import delete
from gateways.sqlalchemy_gateway import get_session
from models import User
from random import randint


@pytest.fixture
def fake_user_data(faker: Faker):
    data = {
        "username": faker.user_name() + str(randint(1, 1000)),
        "phone_number": str(randint(10000, 10000000)),
        "password_hash": faker.password().encode(),
    }
    return data


@pytest_asyncio.fixture
async def test_user(fake_user_data: dict):
    user = User(**fake_user_data)

    async with get_session() as session:
        session.add(user)
    yield user
    async with get_session() as session:
        await session.execute(delete(User).filter_by(id=user.id))
