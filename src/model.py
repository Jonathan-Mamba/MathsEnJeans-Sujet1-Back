import fastapi
import asyncio
import itertools
import uuid
from typing import Iterator
from functools import wraps
from src.datatypes import Player, Day, Route, GameStatus, Square, void_player, StatusDict, RouteType


def in_progress(error_message: str):
    def decorator(func):
        @wraps(func)
        def wrapper(self: 'GameModel', *args, **kwargs):
            if self.status != GameStatus.IN_PROGRESS:
                return func(self, *args, **kwargs)
            raise RuntimeError(error_message) 
        return wrapper
    return decorator


class GameModel:
    def __init__(self):
        self.day_count = 1
        self.current_player = void_player
        self.status: GameStatus = GameStatus.NOT_STARTED
        self.player_iterator: Iterator[tuple[int, Player]] = itertools.cycle(enumerate([void_player]))
        self.players_dict: dict[uuid.UUID, Player] = {}
        self.calendar: list[Day] = []
        self.routes: set[Route] = set()

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
    def remove_player(self, player_id: uuid.UUID):
        try:
            self.players_dict.pop(player_id)
        except KeyError:
            raise RuntimeError("Player not found.")

    @in_progress("Cannot modify players after the game has started.")
    def modify_player(self, player_id: uuid.UUID, new_name: str, new_position: Square):
        if new_position is None:
            raise RuntimeError("Player must have a valid starting position.")   
         
        player = self.get_player(player_id)  
        new_player = Player(name=new_name, position=new_position, id=player_id)
        self.players_dict[player_id] = new_player

    def get_players(self) -> list[Player]:
        return list(self.players_dict.values())
    
    def get_player(self, player_id: uuid.UUID) -> Player:
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
        if route.first_end is None or route.second_end is None:
            raise RuntimeError("Route must have valid endpoints.")
        self.routes.add(route)

    def get_bound_routes(self, square: Square | None) -> set[Route]:
        return {
            route for route in self.routes 
            if (route.first_end == square or route.second_end == square)
            }

    def remove_route(self, route: Route):
        self.routes.remove(route)

    def get_route_types(self) -> list[RouteType]:
        return [route_type for route_type in RouteType]

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
    
    def move_player(self, player_id: uuid.UUID, new_position: Square):
        if self.status != GameStatus.IN_PROGRESS:
            raise RuntimeError("Cannot move players when the game is not in progress.")
        
        player = self.get_player(player_id)
        if player != self.current_player:
            raise RuntimeError("It's not this player's turn.")
        
        route_type = self.calendar[self.day_count - 1]
        routes = self.get_bound_routes(player.position) & self.get_bound_routes(new_position)
        routes = {route for route in routes if (route.type == RouteType.TOUT or route.type == route_type)}
        if not routes:
            raise RuntimeError("No valid route between the two squares.")

        player.position = new_position
        index, self.current_player = next(self.player_iterator)
        if index == 0:
            self.day_count += 1
            if self.day_count > len(self.calendar):
                self.status = GameStatus.COMPLETED

    def get_event(self, request: fastapi.Request):
        async def event_generator():
            day = self.day_count
            while True:
                if await request.is_disconnected():
                    break

                if day != self.day_count:
                    yield {"event": "new_day", "data": self.day_count}
                    day = self.day_count

                if self.status == GameStatus.COMPLETED:
                    yield {"event": "game_finished", "data": "The game has finished."}
                    break

                await asyncio.sleep(0.5)
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
            