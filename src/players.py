import uuid
from fastapi import APIRouter, HTTPException
from typing import List
from .model import GameModelDep
from .datatypes import Player, Square


router = APIRouter(prefix="/players", tags=["players"])


@router.get("/", summary="Get all players", response_model=List[Player])
async def get_all_players(game_model: GameModelDep):
    return game_model.get_players()


@router.post("/", summary="Add a new player")
async def add_player(name: str, game_model: GameModelDep, position: Square):
    try:
        game_model.add_player(Player(name=name, position=Square(position), id=uuid.uuid4()))
    except RuntimeError or ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Player added successfully."


@router.put("/", summary="Update a player's data")
async def update_player(player_id: uuid.UUID, new_name: str, new_position: Square, game_model: GameModelDep):
    try:
        game_model.modify_player(player_id, Player(name=new_name, position=new_position, id=player_id))
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Player updated successfully."


@router.delete("/", summary="Remove a player")
async def remove_player(player_id: uuid.UUID, game_model: GameModelDep):
    try:
        game_model.remove_player(player_id)
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Player removed successfully."
