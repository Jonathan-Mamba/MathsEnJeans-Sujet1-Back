import fastapi
from fastapi import HTTPException
from controller import ControllerDep
from typing import List
from pydantic import BaseModel


class DayCreate(BaseModel):
    day_type: str
 

class DayUpdate(BaseModel):
    day_number: int
    new_day: str


router = fastapi.APIRouter(prefix="/calendar", tags=["calendar"])


@router.get("", response_model=List[str])
def get_calendar(controller: ControllerDep):
    return controller.get_calendar()


@router.get("/day_types", response_model=List[str])
def get_day_types(controller: ControllerDep):
    return controller.get_day_types()


@router.post("")
def add_day(params: DayCreate, controller: ControllerDep):
    try:
        controller.add_day(params.day_type)
    except ValueError as e:
        raise HTTPException(400, str(e))
    return "Day added successfully."


@router.put("")
def modify_day(day: DayUpdate, controller: ControllerDep):
    try:    
        controller.modify_day(day.day_number, day.new_day)
    except IndexError as e:
        raise HTTPException(400, str(e))
    return "Day modified successfully."
    

@router.delete("/{day_number}")
def delete_day(day_number: int, controller: ControllerDep):
    try:
        controller.remove_day(day_number)
    except IndexError as e:
        raise HTTPException(400, str(e))
    return "Day removed successfully."