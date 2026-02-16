import threading
from uuid import UUID
from src.datatypes import Player, Square, Route, Day, StatusDict, RouteType
from src.model import GameModel
from fastapi import Depends
from typing import Annotated


class Controller:
    def __init__(self):
        self._game_model = GameModel()
        self._caldendar_lock = threading.Lock()
        self._players_lock = threading.Lock()
        self._routes_lock = threading.Lock()

    # Game methods
    def game_status(self) -> StatusDict:
        return self._game_model.game_status()
    
    def get_event(self, request):
        return self._game_model.get_event(request)
    
    def start_game(self):
        self._game_model.start_game()

    def move_player(self, player_id: UUID, new_position: Square):
        self._game_model.move_player(player_id, new_position)

    # Player methods
    def get_players(self) -> list[Player]:
        return self._game_model.get_players()

    def add_player(self, player: Player):
        with self._players_lock:
            self._game_model.add_player(player)

    def modify_player(self, player_id: UUID, new_name: str, new_position: Square):
        with self._players_lock:
            self._game_model.modify_player(player_id, new_name, new_position)
    
    def remove_player(self, player_id: UUID):
        with self._players_lock:
            self._game_model.remove_player(player_id)

    # Square methods
    def get_squares(self) -> list[Square]:
        return self._game_model.get_squares()
    
    # Route methods
    def get_all_routes(self) -> list[Route]:
        return self._game_model.get_all_routes()
    
    def add_route(self, route: Route):
        with self._routes_lock:
            self._game_model.add_route(route)

    def remove_route(self, route: Route):
        with self._routes_lock:
            self._game_model.remove_route(route)

    def get_route_types(self) -> list[RouteType]:
        return self._game_model.get_route_types()

    # Calendar methods
    def get_calendar(self) -> list[Day]:
        with self._caldendar_lock:
            return self._game_model.get_calendar()
        
    def add_day(self, day: Day):
        with self._caldendar_lock:
            self._game_model.add_day(day)

    def remove_day(self, day_number: int):
        with self._caldendar_lock:
            self._game_model.remove_day(day_number)

    def modify_day(self, day_number: int, new_day: Day):
        with self._caldendar_lock:
            self._game_model.modify_day(day_number, new_day)

    def get_day_types(self) -> list[Day]:
        return self._game_model.get_day_types()

_controller = Controller()

def get_controller() -> Controller:
    return _controller

ControllerDep = Annotated[Controller, Depends(get_controller)]

    

    