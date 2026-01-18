import fastapi
import uuid
from ..datatypes import Square, StatusDict
from ..controller import ControllerDep
from sse_starlette.sse import EventSourceResponse

router = fastapi.APIRouter(prefix="/game", tags=["game"])

@router.get("/status", response_model=StatusDict)
def get_game_status(controller: ControllerDep):
    return controller.game_status()

@router.post("/move_player")
def move_player(player_id: uuid.UUID, new_position: Square, controller: ControllerDep):
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

@router.get("/events")
def game_events(request: fastapi.Request, controller: ControllerDep):
    return EventSourceResponse(controller.get_event(request))
