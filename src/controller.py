from src.util import Player, Route, StatusDict, GameHistoryEntry, ExportDict
from src.model import GameModel
from fastapi import Depends
from typing import Annotated
from asyncio import Lock
from contextlib import AsyncExitStack


class Controller:
    def __init__(self):
        self._game_model = GameModel()
        
        self._calendar_lock = Lock()
        self._players_lock = Lock()
        self._routes_lock = Lock()
        self._squares_lock = Lock()
        self._game_lock = Lock()

    async def export_model(self) -> ExportDict:
        locks = [
            self._game_lock,
            self._calendar_lock,
            self._players_lock,
            self._routes_lock,
            self._squares_lock
        ]
        async with AsyncExitStack() as stack:
            for lock in locks:
                await stack.enter_async_context(lock)
            
            # All locks are held, safe to export
            return self._game_model.export()
    
    async def import_preset(self):
        locks = [
            self._game_lock,
            self._calendar_lock,
            self._players_lock,
            self._routes_lock,
            self._squares_lock
        ]
        async with AsyncExitStack() as stack:
            for lock in locks:
                await stack.enter_async_context(lock)
            self._game_model.import_preset()

    # Game methods
    async def game_status(self) -> StatusDict:
        locks = [
            self._game_lock,
            self._players_lock,
        ]
        async with AsyncExitStack() as stack:
            for lock in locks:
                await stack.enter_async_context(lock)
            return self._game_model.game_status()
    
    async def start_game(self):
        async with self._game_lock:
             await self._game_model.start_game()

    async def move_player(self, player_id: str, new_position: str):
        async with self._game_lock:
            await self._game_model.move_player(player_id, new_position)

    async def simulate_game(self):
        async with self._game_lock:
            await self._game_model.simulate_game()

    async def get_castle_square(self) -> str:
        async with self._game_lock:
            return self._game_model.castle_square
    
    async def stop_game(self):
        async with self._game_lock:
            await self._game_model.stop_game()

    async def get_game_history(self) -> list[GameHistoryEntry]:
        async with self._game_lock:        
            return self._game_model.game_history

    # Player methods
    async def get_players(self) -> list[Player]:
        async with self._players_lock:
            return self._game_model.get_players()

    async def add_player(self, player: Player):
        async with self._players_lock:
            self._game_model.add_player(player)

    async def modify_player(self, player_id: str, new_name: str, new_position: str):
        async with self._players_lock:
            self._game_model.modify_player(player_id, new_name, new_position)

    async def remove_player(self, player_id: str):
        async with self._players_lock:
            self._game_model.remove_player(player_id)

    # Square methods
    async def get_squares(self) -> list[str]:
        async with self._squares_lock:
            return self._game_model.get_squares()

    async def add_square(self, square: str):
        async with self._squares_lock:    
            self._game_model.add_square(square)

    async def remove_square(self, square: str):
        async with self._squares_lock:
            self._game_model.remove_square(square)

    # Route methods
    async def get_all_routes(self) -> list[Route]:
        async with self._routes_lock:
            return self._game_model.get_all_routes()

    async def add_route(self, route: Route):
        async with self._routes_lock:
            self._game_model.add_route(route)

    async def remove_route(self, route: Route):
        async with self._routes_lock:
            self._game_model.remove_route(route)

    # Route type methods
    async def get_route_types(self) -> dict[str, str]:
        async with self._routes_lock:
            return self._game_model.get_route_types()

    async def add_route_type(self, route_type: str, color: str | None = None):
        async with self._routes_lock:
            self._game_model.add_route_type(route_type, color)

    async def remove_route_type(self, route_type: str):
        async with self._routes_lock:
            self._game_model.remove_route_type(route_type)

    async def get_route_type_all(self) -> str:
        async with self._routes_lock:
            return self._game_model.get_route_type_all()

    # Calendar methods
    async def get_calendar(self) -> list[str]:
        async with self._calendar_lock:
            return self._game_model.get_calendar()
        
    async def add_day(self, day: str):
        async with self._calendar_lock:
            self._game_model.add_day(day)

    async def remove_day(self, day_number: int):
        async with self._calendar_lock:
            self._game_model.remove_day(day_number)

    async def modify_day(self, day_number: int, new_day: str):
        async with self._calendar_lock:
            self._game_model.modify_day(day_number, new_day)

    async def get_day_types(self) -> list[str]:
        async with self._calendar_lock:
            return self._game_model.get_day_types()
    

_controller = Controller()

def get_controller() -> Controller:
    return _controller

ControllerDep = Annotated[Controller, Depends(get_controller)]
