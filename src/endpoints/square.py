from fastapi import APIRouter, Request
import fastapi
from src.controller import ControllerDep
from pydantic import BaseModel
from src.rate_limiter import rate_limit


class SquareCreate(BaseModel):
    name: str


router = APIRouter(prefix="/squares", tags=["squares"])


@rate_limit
@router.get("/", summary="Get all squares", response_model=list[str])
def get_all_squares(request: Request, controller: ControllerDep):
    return controller.get_squares()


@rate_limit
@router.post("/", summary="Add a new square", response_model=str)
def add_square(request: Request, params: SquareCreate, controller: ControllerDep):
    try:
        controller.add_square(params.name)
    except RuntimeError as e:
        raise fastapi.HTTPException(400, str(e))
    return "Square added successfully."


@rate_limit
@router.delete("/", summary="Remove a square")
def remove_square(request: Request, params: SquareCreate, controller: ControllerDep):
    try:
        controller.remove_square(params.name)
    except RuntimeError as e:
        raise fastapi.HTTPException(400, str(e))
    return "Square removed successfully."

@rate_limit
@router.get("/castle", summary="Get the name of the 'castle' square")
def get_castle_square(request: Request, controller: ControllerDep):
    return controller.get_castle_square()
