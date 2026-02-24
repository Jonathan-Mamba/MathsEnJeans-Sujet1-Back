import fastapi
import asyncio
import itertools
import random
from typing import Optional
from pydantic import ValidationError
from functools import wraps
from util import Player, Day, Route, GameStatus, Square, void_player, StatusDict, RouteType, get_random_color, ROUTE_ALL, ExportDict


def in_progress(error_message: str):
    def decorator(func):
        @wraps(func)
        def wrapper(self: 'GameModel', *args, **kwargs):
            if self.status != GameStatus.IN_PROGRESS:
                return func(self, *args, **kwargs)
            raise RuntimeError(error_message) 
        return wrapper
    return decorator


def validate_data(data: dict) -> dict:
    final_dict = {}
    players = data.get("players", [])
    routes = data.get("routes", [])
    route_types = data.get("route_types", [])
    route_type_all = data.get("route_type_all", "")
    route_colors = data.get("route_colors", {})
    game_state = data.get("game_state", {})
    calendar = data.get("calendar", [])
    
    return final_dict

class GameModel:
    def __init__(self):
        self.day_count = 1
        self.current_player = void_player
        self.status = GameStatus.NOT_STARTED
        self.player_iterator = itertools.cycle(enumerate([void_player]))
        self.players_dict: dict[str, Player] = {}
        self.calendar: list[Day] = []
        self.routes: set[Route] = set()
        self.route_types = {i: get_random_color() for i in RouteType}
        self.route_type_all = ROUTE_ALL
        self.castle_square = Square.PALAIS
        self.game_history: list[dict] = []
        self.simulated = False
        self.player_moved = False

   # Player methods    
    @in_progress("Cannot add players after the game has started.")
    def add_player(self, player: Player):
        if player.position is None:
            raise RuntimeError("Player must have a valid starting position.")    
        try:
            self.get_player(player.id)
        except RuntimeError:
            self.players_dict[player.id] = player
        else:
            raise RuntimeError("Player with this ID already exists.")

    @in_progress("Cannot remove players after the game has started.")
    def remove_player(self, player_id: str):
        try:
            self.players_dict.pop(player_id)
        except KeyError:
            raise RuntimeError("Player not found.")

    @in_progress("Cannot modify players after the game has started.")
    def modify_player(self, player_id: str, new_name: str, new_position: Square):
        if new_position is None:
            raise RuntimeError("Player must have a valid starting position.")   
         
        player = self.get_player(player_id)  
        new_player = Player(name=new_name, position=new_position, id=player_id)
        self.players_dict[player_id] = new_player

    def get_players(self) -> list[Player]:
        return list(self.players_dict.values())
    
    def get_player(self, player_id: str) -> Player:
        try:
            return self.players_dict[player_id]
        except KeyError:
            raise RuntimeError("Player not found.")
    
    def get_squares(self) -> list[Square]:
        return [square for square in Square]
    
    # Route methods
    def get_all_routes(self) -> list[Route]:
        return list(self.routes)
    
    @in_progress("Cannot modify routes after the game has started.")
    def add_route(self, route: Route):
        bound_routes = self.get_connected_routes(route.first_end, route.second_end)
        
        if any(r.type == self.route_type_all for r in bound_routes):
            return
        self.routes.add(route)

        bound_routes = self.get_connected_routes(route.first_end, route.second_end)
        route_types = {r.type for r in bound_routes}
        
        if route_types == set(self.get_day_types()):
            for route_type in route_types:
                self.routes.remove(Route(first_end=route.first_end, second_end=route.second_end, type=route_type))
            self.routes.add(Route(first_end=route.first_end, second_end=route.second_end, type=self.route_type_all))


    def get_connected_routes(self, first_square: Square | None, second_square: Square | None = None) -> set[Route]:
        if first_square is None:
            return set()
        if second_square is None:
            return {route for route in self.routes if first_square in (route.first_end, route.second_end)}
        return {route for route in self.routes if {route.first_end, route.second_end} == {first_square, second_square}}


    def remove_route(self, route: Route):
        self.routes.remove(route)

    def get_route_types(self) -> dict[RouteType, str]:
        return self.route_types
    
    def get_route_type_all(self) -> str:
        return self.route_type_all

    # Calendar methods
    def get_calendar(self) -> list[Day]:
        return self.calendar.copy()
    
    @in_progress("Cannot modify calendar after the game has started.")
    def add_day(self, day: Day):
        self.calendar.append(day)
    
    @in_progress("Cannot modify calendar after the game has started.")
    def remove_day(self, day_number: int):
        self.calendar = [day for index, day in enumerate(self.calendar) if index+1 != day_number]

    @in_progress("Cannot modify calendar after the game has started.")
    def modify_day(self, day_number: int, new_day_type: Day):
        if 0 < day_number <= len(self.calendar):
            self.calendar[day_number - 1] = new_day_type
        else:
            raise IndexError("Day number out of range.")
        
    def get_day_types(self) -> list[Day]:
        return [day for day in Day]

    # Game methods
    def game_status(self) -> StatusDict:
        return {
            "status": self.status,
            "day_count": self.day_count,
            "current_player": self.current_player,
            "current_day_type": self.calendar[self.day_count - 1] if self.status == GameStatus.IN_PROGRESS else None
        }
    
    def add_to_history(self, player_id: str, old_position: str, new_position: str):
        if len(self.game_history) < self.day_count:
            self.game_history.append({"day_type": self.calendar[self.day_count - 1], "moves": []})
       
        day_moves = self.game_history[self.day_count - 1]["moves"]
        day_moves.append((player_id, old_position, new_position))

    def simulate_game(self):
        if self.status == GameStatus.NOT_STARTED:
            raise RuntimeError("Connot simulate game if game is not started.")
        
        while self.status == GameStatus.IN_PROGRESS:
            avaialable_squares = [
                (route.first_end if route.second_end == self.current_player.position else route.second_end)
                for route in self.get_connected_routes(self.current_player.position)
            ]
            self.move_player(self.current_player.id, random.choice(avaialable_squares))
    
    def move_player(self, player_id: str, new_position: Square):
        if self.status != GameStatus.IN_PROGRESS:
            raise RuntimeError("Cannot move players when the game is not in progress.")
        
        player = self.get_player(player_id)
        if player != self.current_player:
            raise RuntimeError("It's not this player's turn.")
        
        route_type = self.calendar[self.day_count - 1]
        routes = self.get_connected_routes(player.position, new_position)
        routes = {route for route in routes if (route.type == self.route_type_all or route.type == route_type)}
        if not routes:
            raise RuntimeError("No valid route between the two squares.")

        player.position = new_position
        self.player_moved = True
        self.add_to_history(player_id=player.id, old_position=player.position, new_position=new_position)
        index, self.current_player = next(self.player_iterator)
        if index == 0:
            self.at_new_turn()

    def at_new_turn(self):
        self.day_count += 1
        if self.day_count > len(self.calendar) or all(player.position == self.castle_square for player in self.players_dict.values()) or not self.player_moved:
            self.status = GameStatus.COMPLETED
        else:
            self.player_moved = False

    def get_event(self, request: fastapi.Request):
        async def event_generator():
            day = self.day_count
            player = self.current_player.model_copy()
            while True:
                if await request.is_disconnected():
                    break

                if day != self.day_count:
                    yield {"event": "new_day", "data": self.day_count}
                    day = self.day_count

                if self.status == GameStatus.COMPLETED:
                    yield {"event": "game_finished", "data": "The game has finished."}
                    break

                if player != self.current_player:
                    yield {"event": "player_moved", "data": self.current_player}
                    player = self.current_player.model_copy()

                await asyncio.sleep(0.1)
        return event_generator()
    
    @in_progress("Game has already started.")
    def start_game(self):        
        if not self.players_dict:
            raise RuntimeError("Cannot start game without players.")
        if not self.calendar:
            raise RuntimeError("Cannot start game without a calendar.") 
        if not self.routes:
            raise RuntimeError("Cannot start game without routes.")
        
        self.status = GameStatus.IN_PROGRESS
        self.player_iterator = itertools.cycle(enumerate(self.players_dict.values()))
        index, self.current_player = next(self.player_iterator)

    def export(self) -> dict:
        return {
            "version": "1.0",
            "data": {
                "players": [i.model_dump() for i in self.players_dict.values()],
                "routes": [i.model_dump() for i in self.routes],
                "route_types": list(self.route_types.keys()),
                "route_type_all": self.route_type_all,
                "castle_square": self.castle_square,
                "route_colors": self.route_types,
                "game_state": self.game_status(),
                "calendar": self.calendar,
            }
        }
    
    def import_data(self, imported_dict: ExportDict) -> None:
        version = imported_dict['version']
        if version != "1.0":
            raise RuntimeError(f"Version '{version}' is not supported.")
        

        