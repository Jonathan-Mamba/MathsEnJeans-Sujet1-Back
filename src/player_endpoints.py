import uuid
from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from controller import ControllerDep
from util import Player


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


@router.get("", summary="Get all players", response_model=List[Player])
def get_all_players(controller: ControllerDep):
    return controller.get_players()


@router.post("", summary="Add a new player")
def add_player(params: PlayerCreate, controller: ControllerDep):
    try:
        controller.add_player(Player(name=params.name, position=params.position))
    except RuntimeError or ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Player added successfully."


@router.put("/", summary="Update a player's data")
def update_player(params: PlayerUpdate, controller: ControllerDep):
    try:
        controller.modify_player(params.id, params.name, params.position)
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Player updated successfully."


@router.delete("/", summary="Remove a player")
def remove_player(params: PlayerDelete, controller: ControllerDep):
    try:
        controller.remove_player(params.id)
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Player removed successfully."
