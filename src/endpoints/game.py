import fastapi
from src.util import StatusDict, GameHistoryEntry
from src.controller import ControllerDep
from pydantic import BaseModel
from src.rate_limiter import rate_limit
from src.event_manager import EventManagerDep

class MovePlayer(BaseModel):
    player_id: str
    new_position: str


router = fastapi.APIRouter(prefix="/game", tags=["game"])


@rate_limit
@router.get("/status", response_model=StatusDict)
async def get_game_status(controller: ControllerDep):
    return await controller.game_status()


@rate_limit
@router.post("/move_player")
async def move_player(move: MovePlayer, controller: ControllerDep, event_manager: EventManagerDep):
    try:
        await controller.move_player(move.player_id, move.new_position)
        await event_manager.broadcast_event("game.player.moved", {"id": move.player_id, "position": move.new_position})
    except RuntimeError as e:
        raise fastapi.HTTPException(400, str(e))
    return "Player moved successfully."


@rate_limit
@router.post("/start")
async def start_game(controller: ControllerDep, event_manager: EventManagerDep):
    try:
        await controller.start_game()
        await event_manager.broadcast_event("game.started", {})
    except RuntimeError as e:
        raise fastapi.HTTPException(400, str(e))
    return "Game started successfully."


@rate_limit
@router.post('/end')
async def stop_game(controller: ControllerDep, event_manager: EventManagerDep):
    try:
        await controller.stop_game()
        await event_manager.broadcast_event("game.ended", {})
    except RuntimeError as e:
        raise fastapi.HTTPException(400, str(e))
    return "Game ended successfully."


@rate_limit
@router.post("/simulate")
async def simulate_game(controller: ControllerDep, event_manager: EventManagerDep):
    try:
        await controller.simulate_game()
        await event_manager.broadcast_event("game.simulated", {})
    except RuntimeError as e:
        raise fastapi.HTTPException(400, str(e))
    return "Game simulated successfully."


@rate_limit
@router.get("/history", response_model=list[GameHistoryEntry])
async def get_game_history(controller: ControllerDep):
    return await controller.get_game_history()
