import fastapi
from fastapi import HTTPException
from ..controller import ControllerDep
from ..datatypes import Day
from typing import List

router = fastapi.APIRouter(prefix="/calendar", tags=["calendar"])

@router.get("/", response_model=List[Day])
async def get_calendar(controller: ControllerDep):
    return controller.get_calendar()

@router.post("/")
async def add_day(day_type: Day, controller: ControllerDep):
    try:
        controller.add_day(day_type)
    except ValueError as e:
        raise HTTPException(400, str(e))
    return "Day added successfully."

@router.put("/")
async def modify_day(day_number: int, new_day: Day, controller: ControllerDep):
    try:    
        controller.modify_day(day_number, new_day)
    except IndexError as e:
        raise HTTPException(400, str(e))
    return "Day modified successfully."
    
@router.delete("/")
async def delete_day(day_number: int, controller: ControllerDep):
    controller.remove_day(day_number)
    return "Day removed successfully."