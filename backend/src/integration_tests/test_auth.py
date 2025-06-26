from faker import Faker
import pytest
from httpx import AsyncClient
from sqlalchemy import update
from api.v1.auth import AUTH_TOKEN_KEY
from gateways.sqlalchemy_gateway import get_session
from integration_tests.conftest import shuffle_case
from models import User
from dto import SignInDTO, SignUpDTO


@pytest.mark.asyncio
async def test_signin_success(
    client: AsyncClient, test_user_with_password: tuple[User, str]
):
    expected_user, password = test_user_with_password
    resp = await client.post(
        "/auth/signin",
        json=SignInDTO(
            username=shuffle_case(expected_user.username), password=password
        ).model_dump(mode="json"),
    )
    assert resp.status_code == 200
    assert resp.cookies.get(AUTH_TOKEN_KEY) is not None
    resp_data = resp.json()
    assert resp_data["id"] == expected_user.id


@pytest.mark.asyncio
async def test_signin_invalid_pass(
    client: AsyncClient, test_user_with_password: tuple[User, str]
):
    expected_user, _ = test_user_with_password
    resp = await client.post(
        "/auth/signin",
        json=SignInDTO(
            username=shuffle_case(expected_user.username), password="invalid123"
        ).model_dump(mode="json"),
    )
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_signin_not_found_user(client: AsyncClient, faker: Faker):
    resp = await client.post(
        "/auth/signin",
        json=SignInDTO(
            username=faker.user_name(), password=faker.password(8)
        ).model_dump(mode="json"),
    )
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_signin_not_active_user(
    client: AsyncClient, test_user_with_password: tuple[User, str]
):
    expected_user, password = test_user_with_password
    async with get_session() as session:
        await session.execute(
            update(User).values(is_active=False).filter_by(id=expected_user.id)
        )
    resp = await client.post(
        "/auth/signin",
        json=SignInDTO(
            username=shuffle_case(expected_user.username), password=password
        ).model_dump(mode="json"),
    )
    assert resp.status_code == 403


@pytest.fixture
def fake_signup_dto(faker: Faker):
    return SignUpDTO(
        username=faker.user_name(),
        password=faker.password(),
        phone_number=faker.phone_number(),
    )


@pytest.mark.asyncio
async def test_signup_success(client: AsyncClient, fake_signup_dto: SignUpDTO):
    resp = await client.post(
        "/auth/signup",
        json=fake_signup_dto.model_dump(mode="json"),
    )
    assert resp.status_code == 200
    resp_data = resp.json()
    assert resp_data["username"] == fake_signup_dto.username


@pytest.mark.asyncio
async def test_signup_already_exists(
    client: AsyncClient,
    test_user_with_password: tuple[User, str],
    fake_signup_dto: SignUpDTO,
):
    user, _ = test_user_with_password
    fake_signup_dto.username = user.username
    resp = await client.post(
        "/auth/signup",
        json=fake_signup_dto.model_dump(mode="json"),
    )
    assert resp.status_code == 409
