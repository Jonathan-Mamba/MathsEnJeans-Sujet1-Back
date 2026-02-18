from fastapi import APIRouter
from controller import ControllerDep
from util import Square

router = APIRouter(prefix="/squares", tags=["squares"])

@router.get("/", summary="Get all squares", response_model=list[Square])
def get_all_squares(controller: ControllerDep):
    return controller.get_squares()
