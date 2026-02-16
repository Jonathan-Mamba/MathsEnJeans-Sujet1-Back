from fastapi import APIRouter
from src.controller import ControllerDep
from src.datatypes import Square

router = APIRouter(prefix="/squares", tags=["squares"])

@router.get("/", summary="Get all squares", response_model=list[Square])
def get_all_squares(controller: ControllerDep):
    return controller.get_squares()
