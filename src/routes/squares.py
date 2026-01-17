from fastapi import APIRouter
from ..controller import ControllerDep
from ..datatypes import Square

router = APIRouter(prefix="/squares", tags=["squares"])

@router.get("/", summary="Get all squares", response_model=list[Square])
async def get_all_squares(controller: ControllerDep):
    return controller.get_squares()
