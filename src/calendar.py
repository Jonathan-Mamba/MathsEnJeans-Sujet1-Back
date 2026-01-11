import fastapi
from fastapi import HTTPException
from .model import GameModelDep
from .datatypes import Day
from typing import List

router = fastapi.APIRouter(prefix="/calendar", tags=["calendar"])

@router.get("/", response_model=List[Day])
async def get_calendar(game_model: GameModelDep):
    return game_model.get_calendar()

@router.post("/")
async def add_day(day_type: Day, game_model: GameModelDep):
    try:
        game_model.add_day(day_type)
    except ValueError as e:
        raise HTTPException(400, str(e))
    return "Day added successfully."

@router.put("/")
async def modify_day(day_number: int, new_day: Day, game_model: GameModelDep):
    try:    
        game_model.modify_day(day_number, new_day)
    except IndexError as e:
        raise HTTPException(400, str(e))
    return "Day modified successfully."
    
@router.delete("/")
async def delete_day(day_number: int, game_model: GameModelDep):
    game_model.remove_day(day_number)
    return "Day removed successfully."