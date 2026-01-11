from fastapi import APIRouter, HTTPException
from .model import GameModelDep
from .datatypes import Route, Square, RouteType

router = APIRouter(prefix="/routes", tags=["routes"])

@router.get("/", summary="Get all routes", response_model=list[Route])
async def get_all_routes(game_model: GameModelDep):
    return game_model.get_all_routes()

@router.post("/", summary="Add a new route")
async def add_route(first_end: Square, second_end: Square, route_type: RouteType, game_model: GameModelDep):
    try:
        game_model.add_route(Route(first_end=first_end, second_end=second_end, type=route_type))
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Route added successfully."

@router.delete("/", summary="Remove a route")
async def remove_route(route: Route, game_model: GameModelDep):
    try:
        game_model.remove_route(route)
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Route removed successfully."
