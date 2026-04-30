
from fastapi import APIRouter, Request
from src.controller import ControllerDep
from src.rate_limiter import rate_limit
from typing import AsyncIterable
from fastapi.sse import ServerSentEvent, EventSourceResponse
from src.event_manager import EventManagerDep


router = APIRouter(prefix="", tags=["misc"])


@rate_limit
@router.get("/export", summary="Get the data of the model")
async def export_data(controller: ControllerDep):
    return await controller.export_model()


@rate_limit
@router.get("/events", summary="Stream updates over SSE", response_class=EventSourceResponse)
async def stream_items(request: Request, event_manager: EventManagerDep) -> AsyncIterable[ServerSentEvent]:
    async for event in event_manager.event_generator(request):
        import logging
        logging.info(f"Emitting event: {event}")
        yield event