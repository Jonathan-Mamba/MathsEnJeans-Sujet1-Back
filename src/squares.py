from fastapi import APIRouter
from .model import GameModelDep
from .datatypes import Square

router = APIRouter(prefix="/squares", tags=["squares"])

@router.get("/", summary="Get all squares", response_model=list[Square])
async def get_all_squares(game_model: GameModelDep):
    return game_model.get_squares()
