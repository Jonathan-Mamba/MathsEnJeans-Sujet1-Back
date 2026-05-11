from typing import AsyncIterable
from fastapi import APIRouter, Request, HTTPException
from fastapi.sse import ServerSentEvent, EventSourceResponse
from src.rate_limiter import rate_limit
from src.controller import ControllerDep
from src.event_manager import EventManagerDep
from src.util import ExportData


router = APIRouter(prefix="", tags=["misc"])


@rate_limit
@router.get("/export", summary="Get the data of the model", response_model=ExportData)
async def export_data(controller: ControllerDep):
    return await controller.export_model()


@rate_limit
@router.post("/import", summary="Import game data from json")
async def import_data(data: ExportData, controller: ControllerDep, event_mananger: EventManagerDep):
    try:
        await controller.import_data(data)
        await event_mananger.broadcast_event("game.data.import", {})
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Data imported succesfully."


@rate_limit
@router.get("/events", summary="Stream updates over SSE", response_class=EventSourceResponse)
async def stream_items(request: Request, event_manager: EventManagerDep) -> AsyncIterable[ServerSentEvent]:
    async for event in event_manager.event_generator(request):
        yield event


@rate_limit
@router.post("/preset", summary="Load a preset configuration")
async def load_preset(controller: ControllerDep):
    await controller.import_preset()