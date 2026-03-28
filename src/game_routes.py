import fastapi
from util import Square, StatusDict, GameHistoryEntry
from controller import ControllerDep
from sse_starlette.sse import EventSourceResponse

router = fastapi.APIRouter(prefix="/game", tags=["game"])

@router.get("/status", response_model=StatusDict)
def get_game_status(controller: ControllerDep):
    return controller.game_status()

@router.post("/move_player")
def move_player(player_id: str, new_position: Square, controller: ControllerDep):
    try:
        controller.move_player(player_id, new_position)
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
        controller.start_game()
        controller.simulate_game()
    except RuntimeError as e:
        raise fastapi.HTTPException(400, str(e))
    return "Game simulated successfully."

@router.get("/history", response_model=list[GameHistoryEntry])
def game_history(controller: ControllerDep):
    return controller.get_game_history()

@router.get("/events")
def game_events(request: fastapi.Request, controller: ControllerDep):
    return EventSourceResponse(controller.get_event(request))
