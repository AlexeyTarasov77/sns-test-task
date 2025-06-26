from typing import Annotated
from fastapi import APIRouter, Depends

from api.v1.utils import get_user_id_or_raise
from core.ioc import Inject
from services.telegram import TelegramService

router = APIRouter(prefix="/tg")

TelegramServiceDep = Annotated[TelegramService, Inject(TelegramService)]


@router.get("/chats")
async def list_chats(
    user_id: Annotated[int, Depends(get_user_id_or_raise)], service: TelegramServiceDep
):
    return await service.list_chats(user_id)
