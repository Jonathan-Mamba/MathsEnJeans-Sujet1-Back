from asyncio import Queue
from typing import AsyncGenerator
from fastapi.sse import ServerSentEvent


class EventManager:
    def __init__(self) -> None:
        self._event_queue: Queue[tuple[str, dict]] = Queue()
    
    async def broadcast_event(self, id: str, data: dict):
        await self._event_queue.put((id, data))

    async def event_generator(self) -> AsyncGenerator[ServerSentEvent, None]:
        while True:
            event = await self._event_queue.get()
            yield ServerSentEvent(data=event[1], id=event[0])
