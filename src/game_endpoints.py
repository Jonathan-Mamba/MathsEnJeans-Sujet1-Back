import fastapi
from util import StatusDict, GameHistoryEntry
from controller import ControllerDep
from pydantic import BaseModel


class MovePlayer(BaseModel):
    player_id: str
    new_position: str


router = fastapi.APIRouter(prefix="/game", tags=["game"])


@router.get("/status", response_model=StatusDict)
def get_game_status(controller: ControllerDep):
    return controller.game_status()


@router.post("/move_player")
def move_player(move: MovePlayer, controller: ControllerDep):
    try:
        controller.move_player(move.player_id, move.new_position)
    except RuntimeError as e:
        raise fastapi.HTTPException(400, str(e))
    return "Player moved successfully."


@router.post("/start")
def start_game(controller: ControllerDep):
    try:
        controller.start_game()
    except RuntimeError as e:
        raise fastapi.HTTPException(400, str(e))
    return "Game started successfully."


@router.post('/end')
def stop_game(controller: ControllerDep):
    try:
        controller.stop_game()
    except RuntimeError as e:
        raise fastapi.HTTPException(400, str(e))
    return "Game ended successfully."


@router.post("/simulate")
def simulate_game(controller: ControllerDep):
    try:
        controller.simulate_game()
    except RuntimeError as e:
        raise fastapi.HTTPException(400, str(e))
    return "Game simulated successfully."


@router.get("/history", response_model=list[GameHistoryEntry])
def get_game_history(controller: ControllerDep):
    return controller.get_game_history()
