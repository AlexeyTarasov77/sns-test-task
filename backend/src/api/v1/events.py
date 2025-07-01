import asyncio
import json
from api.v1.utils import get_user_id_or_raise
import logging
from typing import Annotated, Any, NamedTuple
from fastapi import Depends, Request
from sse_starlette import EventSourceResponse, ServerSentEvent

events_queue = asyncio.Queue()


class Event(NamedTuple):
    """
    data: any json serializable object
    name: optional event name
    """

    data: Any
    name: str | None = None


class UserEventEmitter:
    def __init__(self) -> None:
        self._users: dict[int, asyncio.Queue] = {}

    async def emit(self, to_user_id: int, event: Event) -> bool:
        queue = self._users.get(to_user_id)
        if not queue:
            logging.warning("User %s is not listening to server events", to_user_id)
            return False
        await queue.put(event)
        return True

    def create_stream(self, user_id: int, req: Request):
        self._users[user_id] = asyncio.Queue()

        async def streamer():
            while True:
                if await req.is_disconnected():
                    break
                event: Event = await self._users[user_id].get()
                yield ServerSentEvent(data=json.dumps(event.data), event=event.name)

        return streamer

    @property
    def clients_count(self) -> int:
        """Get number of currently connected clients."""
        return len(self._users)


event_emitter = UserEventEmitter()


async def sse_endpoint(
    user_id: Annotated[int, Depends(get_user_id_or_raise)], req: Request
):
    streamer = event_emitter.create_stream(user_id, req)
    return EventSourceResponse(streamer())
