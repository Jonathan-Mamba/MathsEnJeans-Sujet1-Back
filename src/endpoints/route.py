from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.util import Route
from src.controller import ControllerDep
from src.rate_limiter import rate_limit
from src.event_manager import EventManagerDep


class RouteTypeCreate(BaseModel):
    name: str


class RouteCreate(BaseModel):
    first_end: str
    second_end: str
    route_type: str


router = APIRouter(prefix="/routes", tags=["routes"])


@rate_limit
@router.get("/", summary="Get all routes", response_model=list[Route])
async def get_all_routes(controller: ControllerDep):
    return await controller.get_all_routes()


@rate_limit
@router.post("/", summary="Add a new route")
async def add_route(params: RouteCreate, controller: ControllerDep, event_manager: EventManagerDep):
    try:
        route = Route(first_end=params.first_end, second_end=params.second_end, type=params.route_type)
        await controller.add_route(route)
        await event_manager.broadcast_event("game.route.added", {"route": route})
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Route added successfully."


@rate_limit
@router.delete("/", summary="Remove a route")
async def remove_route(params: RouteCreate, controller: ControllerDep, event_manager: EventManagerDep):
    try:
        route = Route(first_end=params.first_end, second_end=params.second_end, type=params.route_type)
        await controller.remove_route(route)
        await event_manager.broadcast_event("game.route.removed", {"route": route})
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Route removed successfully."

