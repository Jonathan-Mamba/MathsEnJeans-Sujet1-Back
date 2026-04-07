import threading
from util import Player, Route, StatusDict, GameHistoryEntry, ExportDict
from model import GameModel
from fastapi import Depends
from typing import Annotated


class Controller:
    def __init__(self):
        self._game_model = GameModel()
        self._calendar_lock = threading.Lock()
        self._players_lock = threading.Lock()
        self._routes_lock = threading.Lock()
        self._squares_lock = threading.Lock()
        self._game_lock = threading.Lock()

    def export_model(self) -> ExportDict:
        return self._game_model.export()
    
    def import_preset(self):
        self._game_model.import_preset()

    # Game methods
    def game_status(self) -> StatusDict:
        return self._game_model.game_status()
    
    def get_event(self, request):
        return self._game_model.get_event(request)
    
    def start_game(self):
        with self._game_lock:
            self._game_model.start_game()

    def move_player(self, player_id: str, new_position: str):
        with self._game_lock:
            self._game_model.move_player(player_id, new_position)

    def simulate_game(self):
        with self._game_lock:
            self._game_model.simulate_game()

    def get_castle_square(self) -> str:
        return self._game_model.castle_square
    
    def stop_game(self):
        with self._game_lock:
            self._game_model.stop_game()

    def get_game_history(self) -> list[GameHistoryEntry]:
        return self._game_model.game_history

    # Player methods
    def get_players(self) -> list[Player]:
        return self._game_model.get_players()

    def add_player(self, player: Player):
        with self._players_lock:
            self._game_model.add_player(player)

    def modify_player(self, player_id: str, new_name: str, new_position: str):
        with self._players_lock:
            self._game_model.modify_player(player_id, new_name, new_position)

    def remove_player(self, player_id: str):
        with self._players_lock:
            self._game_model.remove_player(player_id)

    # Square methods
    def get_squares(self) -> list[str]:
        return self._game_model.get_squares()
    
    def add_square(self, square: str):
        with self._squares_lock:    
            self._game_model.add_square(square)

    def remove_square(self, square: str):
        with self._squares_lock:
            self._game_model.remove_square(square)

    # Route methods
    def get_all_routes(self) -> list[Route]:
        return self._game_model.get_all_routes()
    
    def add_route(self, route: Route):
        with self._routes_lock:
            self._game_model.add_route(route)

    def remove_route(self, route: Route):
        with self._routes_lock:
            self._game_model.remove_route(route)

    # Route type methods
    def get_route_types(self) -> dict[str, str]:
        return self._game_model.get_route_types()

    def add_route_type(self, route_type: str, color: str):
        with self._routes_lock:
            self._game_model.add_route_type(route_type)

    def remove_route_type(self, route_type: str):
        with self._routes_lock:
            self._game_model.remove_route_type(route_type)

    def get_route_type_all(self) -> str:
        return self._game_model.get_route_type_all()

    # Calendar methods
    def get_calendar(self) -> list[str]:
        with self._calendar_lock:
            return self._game_model.get_calendar()
        
    def add_day(self, day: str):
        with self._calendar_lock:
            self._game_model.add_day(day)

    def remove_day(self, day_number: int):
        with self._calendar_lock:
            self._game_model.remove_day(day_number)

    def modify_day(self, day_number: int, new_day: str):
        with self._calendar_lock:
            self._game_model.modify_day(day_number, new_day)

    def get_day_types(self) -> list[str]:
        return self._game_model.get_day_types()

_controller = Controller()

def get_controller() -> Controller:
    return _controller

ControllerDep = Annotated[Controller, Depends(get_controller)]
