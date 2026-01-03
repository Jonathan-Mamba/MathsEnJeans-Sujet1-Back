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
async def add_player(name: str, game_model: GameModelDep, position: str = Square.NONE):
    try:
        game_model.add_player(Player(name=name, position=Square(position), id=str(uuid.uuid4())))
    except RuntimeError or ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Player added successfully."}


@router.put("/", summary="Update a player's data")
async def update_player(player_id: str, new_player: Player, game_model: GameModelDep):
    try:
        game_model.modify_player(player_id, new_player)
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Player updated successfully."}


@router.delete("/", summary="Remove a player")
async def remove_player(player_id: str, game_model: GameModelDep):
    try:
        game_model.remove_player(player_id)
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Player removed successfully."}
