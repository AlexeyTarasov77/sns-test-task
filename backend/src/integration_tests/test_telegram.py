from httpx import AsyncClient
from models import User
import pytest


@pytest.mark.asyncio
async def test_list_chats_unauthorized(client: AsyncClient):
    resp = await client.get("/tg/chats")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_list_chats_no_tg_acc(auth_client_with_user: tuple[AsyncClient, User]):
    client, _ = auth_client_with_user
    resp = await client.get("/tg/chats")
    assert resp.status_code == 404
