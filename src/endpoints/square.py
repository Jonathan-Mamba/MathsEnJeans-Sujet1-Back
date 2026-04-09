from fastapi import APIRouter
import fastapi
from src.controller import ControllerDep
from pydantic import BaseModel


class SquareCreate(BaseModel):
    name: str


router = APIRouter(prefix="/squares", tags=["squares"])


@router.get("/", summary="Get all squares", response_model=list[str])
def get_all_squares(controller: ControllerDep):
    return controller.get_squares()


@router.post("/", summary="Add a new square", response_model=str)
def add_square(params: SquareCreate, controller: ControllerDep):
    try:
        controller.add_square(params.name)
    except RuntimeError as e:
        raise fastapi.HTTPException(400, str(e))
    return "Square added successfully."


@router.delete("/", summary="Remove a square")
def remove_square(params: SquareCreate, controller: ControllerDep):
    try:
        controller.remove_square(params.name)
    except RuntimeError as e:
        raise fastapi.HTTPException(400, str(e))
    return "Square removed successfully."


@router.get("/castle", summary="Get the name of the 'castle' square")
def get_castle_square(controller: ControllerDep):
    return controller.get_castle_square()
