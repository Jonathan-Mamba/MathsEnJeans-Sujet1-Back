import fastapi
from .datatypes import Square, StatusDict
from .model import GameModelDep
from sse_starlette.sse import EventSourceResponse

router = fastapi.APIRouter(prefix="/game", tags=["game"])

@router.get("/status", response_model=StatusDict)
async def get_game_status(game_model: GameModelDep):
    return game_model.game_status()

@router.post("/move_player")
async def move_player(player_id: int, new_position: str, game_model: GameModelDep):
    try:
        game_model.move_player(player_id, Square(new_position))
    except RuntimeError as e:
        raise fastapi.HTTPException(400, str(e))
    return {"message": "Player moved successfully."}

@router.post("/start")
async def start_game(game_model: GameModelDep):
    try:
        game_model.start_game()
    except RuntimeError as e:
        raise fastapi.HTTPException(400, str(e))
    return {"message": "Game started successfully."}

@router.get("/events")
async def game_events(request: fastapi.Request, game_model: GameModelDep):
    return EventSourceResponse(game_model.get_event(request))