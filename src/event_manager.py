import asyncio
from typing import AsyncGenerator, Annotated
from fastapi import Request, Depends
from fastapi.sse import ServerSentEvent


class EventManager:
    def __init__(self) -> None:
        self._subscribers: set[asyncio.Queue[tuple[str, dict]]] = set()  # Track all subscribers
    
    async def broadcast_event(self, event_type: str, data: dict):
        for queue in self._subscribers:
            await queue.put((event_type, data))
    
    async def event_generator(self, request: Request) -> AsyncGenerator[ServerSentEvent, None]:
        personal_queue = asyncio.Queue[tuple[str, dict]]()
        self._subscribers.add(personal_queue)
        try:
            while True:
                if await request.is_disconnected():
                    break
                try:
                    event_tuple = await asyncio.wait_for(personal_queue.get(), timeout=1.0)
                except asyncio.TimeoutError:
                    continue
                yield ServerSentEvent(event=event_tuple[0], data=event_tuple[1])
        finally:
            self._subscribers.discard(personal_queue) 


_event_manager = EventManager()

def get_event_manager() -> EventManager:
    return _event_manager

EventManagerDep = Annotated[EventManager, Depends(get_event_manager)]