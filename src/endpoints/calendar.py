import fastapi
from fastapi import HTTPException, Request
from src.controller import ControllerDep
from src.rate_limiter import rate_limit
from typing import List
from pydantic import BaseModel


class DayCreate(BaseModel):
    day_type: str
 

class DayUpdate(BaseModel):
    day_number: int
    day_type: str


router = fastapi.APIRouter(prefix="/calendar", tags=["calendar"])


@rate_limit
@router.get("/", response_model=List[str], summary="Get the calendar, as a list of day types")
def get_calendar(request: Request, controller: ControllerDep):
    return controller.get_calendar()


@rate_limit
@router.get("/day_types", response_model=List[str], summary="Get all day types")
def get_day_types(request: Request, controller: ControllerDep):
    return controller.get_day_types()


@rate_limit
@router.post("/", summary="Add a new day")
def add_day(request: Request, params: DayCreate, controller: ControllerDep):
    try:
        controller.add_day(params.day_type)
    except RuntimeError as e:
        raise HTTPException(400, str(e))
    return "Day added successfully."

@rate_limit
@router.put("/", summary="Modify a day")
def modify_day(request: Request, day: DayUpdate, controller: ControllerDep):
    try:    
        controller.modify_day(day.day_number, day.day_type)
    except IndexError as e:
        raise HTTPException(400, str(e))
    return "Day modified successfully."
    

@rate_limit
@router.delete("/{day_number}", summary="Remove a day")
def delete_day(request: Request, day_number: int, controller: ControllerDep):
    try:
        controller.remove_day(day_number)
    except IndexError as e:
        raise HTTPException(400, str(e))
    return "Day removed successfully."