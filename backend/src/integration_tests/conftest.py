from time import time
from core.config import app_config
from httpx import AsyncClient
import pytest_asyncio
import pytest
from faker import Faker
from gateways.security.hashing import BcryptHasher
from sqlalchemy import delete
from gateways.sqlalchemy_gateway import get_session
from models import User
from random import randint

API_BASE_URL = f"http://localhost:{app_config.server.port}/api/v1"


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(base_url=API_BASE_URL) as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
def faker_seed():
    return time()


@pytest.fixture
def fake_user_data(faker: Faker):
    plain_password = faker.password()
    data = {
        "username": faker.user_name(),
        "phone_number": str(randint(10000, 10000000)),
        "password_hash": BcryptHasher().hash(plain_password),
    }
    return plain_password, data


@pytest_asyncio.fixture
async def test_user_with_password(fake_user_data):
    password, data = fake_user_data
    user = User(**data)

    async with get_session() as session:
        session.add(user)
    yield user, password
    async with get_session() as session:
        await session.execute(delete(User).filter_by(id=user.id))


def shuffle_case(s: str) -> str:
    """Utillity function to shuffle characters case in a string.
    Can be usefull to verify case-insesitivity"""
    shuffled = ""
    for i, ch in enumerate(s):
        if i % 2 == 0:
            shuffled += ch.upper()
        else:
            shuffled += ch.lower()
    return shuffled
