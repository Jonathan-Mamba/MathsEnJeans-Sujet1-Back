from fastapi import APIRouter, HTTPException, Request
from src.controller import ControllerDep
from src.util import Route
from pydantic import BaseModel
from src.rate_limiter import rate_limit


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
async def add_route(params: RouteCreate, controller: ControllerDep):
    try:
        route = Route(first_end=params.first_end, second_end=params.second_end, type=params.route_type)
        await controller.add_route(route)
        await controller.get_event_manager().broadcast_event("game.route.added", {"route": route.model_dump()})
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Route added successfully."


@rate_limit
@router.delete("/", summary="Remove a route")
async def remove_route(params: RouteCreate, controller: ControllerDep):
    try:
        route = Route(first_end=params.first_end, second_end=params.second_end, type=params.route_type)
        await controller.remove_route(route)
        await controller.get_event_manager().broadcast_event("game.route.removed", {"route": route.model_dump()})
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Route removed successfully."


# Route types endpoints
@rate_limit
@router.get("/types", summary="Get all route types, and their colors", response_model=dict[str, str])
async def get_route_types(controller: ControllerDep):
    return await controller.get_route_types()


@rate_limit
@router.post("/types", summary="Add a new route type")
async def add_route_type(params: RouteTypeCreate, controller: ControllerDep):
    try:
        await controller.add_route_type(params.name, "")
        await controller.get_event_manager().broadcast_event("game.route.type.added", {"name": params.name})
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Route type added successfully."


@rate_limit
@router.delete("/types/", summary="Remove a route type")
async def remove_route_type(params: RouteTypeCreate, controller: ControllerDep):
    try:
        await controller.remove_route_type(params.name)
        await controller.get_event_manager().broadcast_event("game.route.type.removed", {"name": params.name})
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Route type removed successfully."


@rate_limit
@router.get("/types/all", summary="Get the name of route type that contains all of the routes.", response_model=str)
async def get_route_type_all(controller: ControllerDep):
    return await controller.get_route_type_all()
