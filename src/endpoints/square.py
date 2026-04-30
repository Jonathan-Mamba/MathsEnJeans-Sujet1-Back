import fastapi
from fastapi import APIRouter
from pydantic import BaseModel
from src.controller import ControllerDep
from src.rate_limiter import rate_limit
from src.event_manager import EventManagerDep


class SquareCreate(BaseModel):
    name: str


router = APIRouter(prefix="/squares", tags=["squares"])


@rate_limit
@router.get("/", summary="Get all squares", response_model=list[str])
async def get_all_squares(controller: ControllerDep):
    return await controller.get_squares()


@rate_limit
@router.post("/", summary="Add a new square", response_model=str)
async def add_square(params: SquareCreate, controller: ControllerDep, event_manager: EventManagerDep):
    try:
        await controller.add_square(params.name)
        await event_manager.broadcast_event("game.square.added", {"name": params.name})
    except RuntimeError as e:
        raise fastapi.HTTPException(400, str(e))
    return "Square added successfully."


@rate_limit
@router.delete("/", summary="Remove a square")
async def remove_square(params: SquareCreate, controller: ControllerDep, event_manager: EventManagerDep):
    try:
        await controller.remove_square(params.name)
        await event_manager.broadcast_event("game.square.removed", {"name": params.name})
    except RuntimeError as e:
        raise fastapi.HTTPException(400, str(e))
    return "Square removed successfully."

@rate_limit
@router.get("/castle", summary="Get the name of the 'castle' square")
async def get_castle_square(controller: ControllerDep):
    return await controller.get_castle_square()
