from typing import Annotated
from fastapi import APIRouter, Depends, status, BackgroundTasks
from gateways.exceptions import StorageNotFoundError
from dto import (
    TgConnectRequestDTO,
    TgConnectConfirmDTO,
    UserTelegramAccDTO,
    TelegramChatDTO,
)
from api.v1.utils import get_user_id_or_raise
from api.v1.events import event_emitter
from core.ioc import Inject
from gateways.contracts import IKeyValueStorage
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
    kv_storage: Annotated[IKeyValueStorage, Inject(IKeyValueStorage)],
):
    # TODO: There is no sense of emitting to specific user, it would be better to make broadcasting
    # since multiple clients can listen to messages of specific chat by event name
    messages_chunk_size = 50
    chat, message_reader = await service.get_chat(user_id, id, messages_chunk_size)
    message_stream_started_key = f"message_stream_started_{user_id}_{chat.id}"

    async def send_messages_stream():
        try:
            print("START STREAMING MESSAGES")
            chunk_generator = message_reader.yield_all_messages(
                chat.id, messages_chunk_size, chat.messages[-1].id
            )
            async for chunk in chunk_generator:
                print("EMITTING NEW CHUNK", len(chunk), chunk[:3])
                emitted = await event_emitter.emit(
                    user_id,
                    [msg.model_dump(mode="json") for msg in chunk],
                    f"chat_{chat.id}_messages",
                )
                print("IS EMITTED", emitted)
                if not emitted:
                    break
            # send empty list to indicate end of message stream
            await event_emitter.emit(user_id, [])
        finally:
            await kv_storage.delete(message_stream_started_key)

    # avoid streaming messages twice to the same client
    try:
        await kv_storage.get(message_stream_started_key)
    except StorageNotFoundError:
        await kv_storage.set(message_stream_started_key, True)
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
