from fastapi import APIRouter, HTTPException, Request
from typing import List
from pydantic import BaseModel
from src.controller import ControllerDep
from src.util import Player
from src.rate_limiter import rate_limit
from src.event_manager import EventManagerDep


class PlayerCreate(BaseModel):
    name: str
    position: str

class PlayerUpdate(BaseModel):
    id: str
    name: str
    position: str

class PlayerDelete(BaseModel):
    id: str


router = APIRouter(prefix="/players", tags=["players"])

@rate_limit
@router.get("/", summary="Get all players", response_model=List[Player])
async def get_all_players(controller: ControllerDep):
    return await controller.get_players()


@rate_limit
@router.post("/", summary="Add a new player")
async def add_player(params: PlayerCreate, controller: ControllerDep, event_manager: EventManagerDep):
    try:
        player = Player(name=params.name, position=params.position)
        await controller.add_player(player)
        await event_manager.broadcast_event("game.player.added", {"player": player.model_dump()})
    except RuntimeError or ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Player added successfully."


@rate_limit
@router.put("/", summary="Update a player's data")
async def update_player(params: PlayerUpdate, controller: ControllerDep, event_manager: EventManagerDep):
    try:
        await controller.modify_player(params.id, params.name, params.position)
        await event_manager.broadcast_event("game.player.modified", {
            "player": [p for p in await controller.get_players() if p.id == params.id][0]
        })
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Player updated successfully."


@rate_limit
@router.delete("/", summary="Remove a player")
async def remove_player(params: PlayerDelete, controller: ControllerDep, event_manager: EventManagerDep):
    try:
        await controller.remove_player(params.id)
        await event_manager.broadcast_event("game.player.removed", {"id": params.id})
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Player removed successfully."
