import logging
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
from api.v1.events import Event, event_emitter
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
    messages_chunk_size = 50
    chat, message_reader = await service.get_chat(user_id, id, messages_chunk_size)
    # user_id must be included in key, because if stream is already running for same chat
    # but client started listening later - he won't receive all messages.
    # So for every new user - new stream should be started
    is_stream_running_key = f"message_stream_running_{user_id}_{chat.id}"
    event_name = f"chat_{chat.id}_messages"

    async def send_messages_stream():
        try:
            chunk_generator = message_reader.yield_all_messages(
                chat.id, messages_chunk_size, chat.messages[-1].id
            )
            async for chunk in chunk_generator:
                logging.info("emitting new messages chunk. Size: %d", len(chunk))
                emitted = await event_emitter.emit(
                    user_id,
                    Event([msg.model_dump(mode="json") for msg in chunk], event_name),
                )
                if not emitted:
                    logging.warning(
                        "Stopped emitting messages because they can't be delivered"
                    )
                    break
            # send empty list to indicate end of message stream
            await event_emitter.emit(user_id, Event([], event_name))
        finally:
            await kv_storage.delete(is_stream_running_key)

    # don't stream messages if not clients are connected
    if event_emitter.clients_count == 0:
        logging.warning("No clients to stream messages for")
        return chat
    # avoid streaming messages twice to the same client
    try:
        await kv_storage.get(is_stream_running_key)
    except StorageNotFoundError:
        await kv_storage.set(is_stream_running_key, True)
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
