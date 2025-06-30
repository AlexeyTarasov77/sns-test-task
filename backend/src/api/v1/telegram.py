from typing import Annotated
from fastapi import APIRouter, Depends, status, BackgroundTasks
from dto import (
    TgConnectRequestDTO,
    TgConnectConfirmDTO,
    UserTelegramAccDTO,
    TelegramChatDTO,
)
from api.v1.utils import get_user_id_or_raise
from api.v1.events import EventEmitterDep
from core.ioc import Inject
from services.telegram import TelegramService

router = APIRouter(prefix="/tg")

TelegramServiceDep = Annotated[TelegramService, Inject(TelegramService)]


@router.get("/chats")
async def list_chats(
    user_id: Annotated[int, Depends(get_user_id_or_raise)], service: TelegramServiceDep
) -> list[TelegramChatDTO]:
    return await service.list_chats(user_id)


@router.get("/chats/{id}")
async def get_chat(
    id: int,
    user_id: Annotated[int, Depends(get_user_id_or_raise)],
    service: TelegramServiceDep,
    background_tasks: BackgroundTasks,
    event_emitter: EventEmitterDep,
):
    # 1. При первом получении чата получается первая партия сообщений - x,
    # и по возможности кол-во всех сообщений в чате
    # 2. После возврата респонса в фоне начинается стриминг оставшихся сообщений по частям,
    # пока все не будут отправлены (x, x+=msg_chunk_size]
    chat, message_reader = await service.get_chat(user_id, id)

    async def send_messages_stream():
        last_msg_id = chat.messages[-1].id
        msg_chunk_size = 50
        while True:
            print("START STREAMING MESSAGES")
            messages = await message_reader.get_messages(
                chat.id, msg_chunk_size, last_msg_id
            )
            print("GOT MESSAGES CHUNK OF SIZE", len(messages))
            if not messages:
                break
            last_msg_id = messages[-1].id
            await event_emitter.emit(
                user_id, [msg.model_dump(mode="json") for msg in messages]
            )

    background_tasks.add_task(send_messages_stream)
    return chat


@router.post("/connect/request")
async def request_tg_connect(
    user_id: Annotated[int, Depends(get_user_id_or_raise)],
    dto: TgConnectRequestDTO,
    service: TelegramServiceDep,
):
    return await service.request_tg_connect(user_id, dto)


@router.delete("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def remove_tg_acc(
    user_id: Annotated[int, Depends(get_user_id_or_raise)], service: TelegramServiceDep
):
    await service.remove_tg_acc(user_id)


@router.post("/connect/confirm")
async def confirm_tg_connect(
    user_id: Annotated[int, Depends(get_user_id_or_raise)],
    dto: TgConnectConfirmDTO,
    service: TelegramServiceDep,
) -> UserTelegramAccDTO:
    return await service.confirm_tg_connect(user_id, dto)
