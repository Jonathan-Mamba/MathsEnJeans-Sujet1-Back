from fastapi import APIRouter
from controller import ControllerDep

router = APIRouter(prefix="/squares", tags=["squares"])

@router.get("", summary="Get all squares", response_model=list[str])
def get_all_squares(controller: ControllerDep):
    return controller.get_squares()

@router.get("/castle", summary="Get the name of the 'castle' square", tags=["squares"])
def get_castle_square(controller: ControllerDep):
    return controller.get_castle_square()
