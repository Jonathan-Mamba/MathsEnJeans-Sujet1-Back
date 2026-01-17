import uuid
from fastapi import APIRouter, HTTPException
from typing import List
from ..controller import ControllerDep
from ..datatypes import Player, Square


router = APIRouter(prefix="/players", tags=["players"])


@router.get("/", summary="Get all players", response_model=List[Player])
async def get_all_players(controller: ControllerDep):
    return controller.get_players()


@router.post("/", summary="Add a new player")
async def add_player(name: str, controller: ControllerDep, position: Square):
    try:
        controller.add_player(Player(name=name, position=Square(position), id=uuid.uuid4()))
    except RuntimeError or ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Player added successfully."


@router.put("/", summary="Update a player's data")
async def update_player(player_id: uuid.UUID, new_name: str, new_position: Square, controller: ControllerDep):
    try:
        controller.modify_player(player_id, Player(name=new_name, position=new_position, id=player_id))
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Player updated successfully."


@router.delete("/", summary="Remove a player")
async def remove_player(player_id: uuid.UUID, controller: ControllerDep):
    try:
        controller.remove_player(player_id)
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Player removed successfully."
