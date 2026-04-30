import fastapi
from fastapi import HTTPException
from src.controller import ControllerDep
from src.rate_limiter import rate_limit
from typing import List
from pydantic import BaseModel
from src.event_manager import EventManagerDep


class DayCreate(BaseModel):
    day_type: str
 

class DayUpdate(BaseModel):
    day_number: int
    day_type: str


router = fastapi.APIRouter(prefix="/calendar", tags=["calendar"])


@rate_limit
@router.get("/", response_model=List[str], summary="Get the calendar, as a list of day types")
async def get_calendar(controller: ControllerDep):
    return await controller.get_calendar()


@rate_limit
@router.get("/day_types", response_model=List[str], summary="Get all day types")
async def get_day_types(controller: ControllerDep):
    return await controller.get_day_types()


@rate_limit
@router.post("/", summary="Add a new day")
async def add_day(params: DayCreate, controller: ControllerDep, event_manager: EventManagerDep):
    try:
        await controller.add_day(params.day_type)
        await event_manager.broadcast_event("game.calendar.added", {"type": params.day_type})
    except RuntimeError as e:
        raise HTTPException(400, str(e))
    return "Day added successfully."

@rate_limit
@router.put("/", summary="Modify a day")
async def modify_day(day: DayUpdate, controller: ControllerDep, event_manager: EventManagerDep):
    try:    
        await controller.modify_day(day.day_number, day.day_type)
        await event_manager.broadcast_event("game.calendar.modified", {"number": day.day_number, "type": day.day_type})
    except IndexError as e:
        raise HTTPException(400, str(e))
    return "Day modified successfully."
    

@rate_limit
@router.delete("/{day_number}", summary="Remove a day")
async def delete_day(day_number: int, controller: ControllerDep, event_manager: EventManagerDep ):
    try:
        await controller.remove_day(day_number)
        await event_manager.broadcast_event("game.calendar.removed", {"number": day_number})
    except IndexError as e:
        raise HTTPException(400, str(e))
    return "Day removed successfully."