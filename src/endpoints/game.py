import fastapi
from src.util import StatusDict, GameHistoryEntry
from src.controller import ControllerDep
from pydantic import BaseModel
from fastapi import Request
from src.rate_limiter import rate_limit

class MovePlayer(BaseModel):
    player_id: str
    new_position: str


router = fastapi.APIRouter(prefix="/game", tags=["game"])


@rate_limit
@router.get("/status", response_model=StatusDict)
def get_game_status(request: Request, controller: ControllerDep):
    return controller.game_status()


@rate_limit
@router.post("/move_player")
def move_player(request: Request, move: MovePlayer, controller: ControllerDep):
    try:
        controller.move_player(move.player_id, move.new_position)
    except RuntimeError as e:
        raise fastapi.HTTPException(400, str(e))
    return "Player moved successfully."


@rate_limit
@router.post("/start")
def start_game(request: Request, controller: ControllerDep):
    try:
        controller.start_game()
    except RuntimeError as e:
        raise fastapi.HTTPException(400, str(e))
    return "Game started successfully."


@rate_limit
@router.post('/end')
def stop_game(request: Request, controller: ControllerDep):
    try:
        controller.stop_game()
    except RuntimeError as e:
        raise fastapi.HTTPException(400, str(e))
    return "Game ended successfully."


@rate_limit
@router.post("/simulate")
def simulate_game(request: Request, controller: ControllerDep):
    try:
        controller.simulate_game()
    except RuntimeError as e:
        raise fastapi.HTTPException(400, str(e))
    return "Game simulated successfully."


@rate_limit
@router.get("/history", response_model=list[GameHistoryEntry])
def get_game_history(request: Request, controller: ControllerDep):
    return controller.get_game_history()
