from fastapi import APIRouter, HTTPException
from .model import GameModelDep
from .datatypes import Route

router = APIRouter(prefix="/routes", tags=["routes"])

@router.get("/", summary="Get all routes", response_model=list[Route])
async def get_all_routes(game_model: GameModelDep):
    return game_model.get_routes()

@router.post("/", summary="Add a new route")
async def add_route(route: Route, game_model: GameModelDep):
    try:
        game_model.add_route(route)
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Route added successfully."}

@router.delete("/", summary="Remove a route")
async def remove_route(route: Route, game_model: GameModelDep):
    try:
        game_model.remove_route(route)
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Route removed successfully."}
