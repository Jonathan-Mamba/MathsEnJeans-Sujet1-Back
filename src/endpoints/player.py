import uuid
from fastapi import APIRouter, HTTPException, Request
from typing import List
from pydantic import BaseModel
from src.controller import ControllerDep
from src.util import Player
from src.rate_limiter import rate_limit


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
def get_all_players(request: Request, controller: ControllerDep):
    return controller.get_players()


@rate_limit
@router.post("/", summary="Add a new player")
def add_player(request: Request, params: PlayerCreate, controller: ControllerDep):
    try:
        controller.add_player(Player(name=params.name, position=params.position))
    except RuntimeError or ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Player added successfully."


@rate_limit
@router.put("/", summary="Update a player's data")
def update_player(request: Request, params: PlayerUpdate, controller: ControllerDep):
    try:
        controller.modify_player(params.id, params.name, params.position)
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Player updated successfully."


@rate_limit
@router.delete("/", summary="Remove a player")
def remove_player(request: Request, params: PlayerDelete, controller: ControllerDep):
    try:
        controller.remove_player(params.id)
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Player removed successfully."
