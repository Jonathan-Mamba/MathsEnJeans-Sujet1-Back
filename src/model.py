import random
from functools import wraps
from itertools import cycle
from src.util import Player, Route, GameStatus, StatusDict, ExportData, GameHistoryEntry


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
        self.day_count = 0
        self.current_player: Player | None = None
        self.status = GameStatus.NOT_STARTED
        self.game_history: list[GameHistoryEntry] = []
        self.simulated = False

        self.player_iterator: cycle[tuple[int, Player]] = cycle(enumerate([]))
        self.players_dict: dict[str, Player] = {}

        self.calendar: list[str] = []
        self.routes: set[Route] = set()
        self.route_types: tuple[str, str, str, str, str] = ("Livraison", "Doléances", "Marchands", "Labeur", "Tout")
        self.route_type_all = "Tout"

        self.castle_square = "Palais"
        self.squares: list[str] = ["Entrepôts royaux", "Quartier des artisants", "Quartier des marchands", "Salle des gardes", "Palais"]


    def import_preset(self):
        new_model = GameModel()
        player1 = Player(position="Quartier des artisants", name="j1")
        player2 = Player(position="Entrepôts royaux", name="j2")

        self.day_count = new_model.day_count
        self.current_player = None
        self.status = new_model.status
        self.player_iterator = new_model.player_iterator
        self.players_dict = {
            player1.id: player1,
            player2.id: player2
        }
        self.calendar = ["Doléances", "Labeur", "Livraison", "Marchands", "Doléances"]
        t = "Tout"
        self.routes = {
            Route(first_end="Quartier des artisants", second_end="Entrepôts royaux", type=t),
            Route(first_end="Entrepôts royaux", second_end="Salle des gardes", type=t),
            Route(first_end="Salle des gardes", second_end="Quartier des marchands", type=t),
            Route(first_end="Quartier des marchands", second_end="Palais", type=t)
        }

   # Player methods ----------------------------------------------------------------------    
    @in_progress("Cannot add players after the game has started.")
    def add_player(self, player: Player):
        if player.name.strip() == "":
            raise RuntimeError("Player name cannot be empty.")
        if player.position is None or player.position not in self.squares:
            raise RuntimeError("Player must have a valid starting position.")
        player_names = {p.name for p in self.players_dict.values()}
        if player.name in player_names:
            raise RuntimeError("Player with this name already exists.")    
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
    def modify_player(self, player_id: str, new_name: str, new_position: str):
        if new_position is None:
            raise RuntimeError("Player must have a valid starting position.")   
        player_names = {p.name for p in self.players_dict.values() if p.id != player_id}
        if new_name in player_names:
            raise RuntimeError("Player with this name already exists.") 

        player = self.get_player(player_id)  
        player.name = new_name
        player.position = new_position

    def get_players(self) -> list[Player]:
        return list(self.players_dict.values())
    
    def get_player(self, player_id: str) -> Player:
        try:
            return self.players_dict[player_id]
        except KeyError:
            raise RuntimeError("Player not found.")
    
    # Square methods ----------------------------------------------------------------------
    def get_squares(self) -> list[str]:
        return list(self.squares)
    
    @in_progress("Cannot modify squares after the game has started.")
    def add_square(self, square: str):
        if square in self.squares:
            raise RuntimeError("Square already exists.")
        if square.strip() == "":
            raise RuntimeError("Square name cannot be empty.")
        if len(self.squares) >= 12:
            raise RuntimeError("Cannot have more than 12 squares.")
        self.squares.append(square)

    @in_progress("Cannot modify squares after the game has started.")
    def modify_square(self, old_name: str, new_name: str):
        if old_name not in self.squares:
            raise RuntimeError("Square not found.")
        if new_name in self.squares:
            raise RuntimeError("Square already exists.")
        if new_name.strip() == "":
            raise RuntimeError("Square name cannot be empty.")
        for player in self.players_dict.values():
            if player.position == old_name:
                player.position = new_name
        for route in self.get_connected_routes(old_name):
            self.routes.remove(route)
            self.routes.add(Route(
                first_end=new_name if route.first_end == old_name else route.first_end,
                second_end=new_name if route.second_end == old_name else route.second_end,
                type=route.type
            ))
        if self.castle_square == old_name:
            self.castle_square = new_name
        self.squares.remove(old_name)
        self.squares.append(new_name)

    @in_progress("Cannot modify squares after the game has started.")
    def remove_square(self, square: str):
        if square == self.castle_square:
            raise RuntimeError("Cannot remove the castle square.")
        if square not in self.squares:
            raise RuntimeError("Square not found.")
        if any(player.position == square for player in self.players_dict.values()):
            raise RuntimeError("Cannot remove a square that has players on it.")
        self.squares.remove(square)
        for route in self.get_connected_routes(square):
            self.routes.remove(route)
    
    def get_castle_square(self) -> str:
        return self.castle_square
    
    @in_progress("Cannot modify castle square after the game has started.")
    def set_castle_square(self, square: str):
        if square not in self.squares:
            raise RuntimeError("Square not found.")
        self.castle_square = square
    
    # Route methods ----------------------------------------------------------------------
    def get_all_routes(self) -> list[Route]:
        return list(self.routes)
    
    @in_progress("Cannot modify routes after the game has started.")
    def add_route(self, added_route: Route):
        if added_route.first_end not in self.squares or added_route.second_end not in self.squares:
            raise RuntimeError("Invalid route ends.")
        
        if added_route.type not in self.route_types:
            raise RuntimeError("Invalid route type.")

        if added_route in self.routes:
            raise RuntimeError("Route already exists.")

        bound_routes = self.get_connected_routes(added_route.first_end, added_route.second_end)
        
        if any(r.type == self.route_type_all for r in bound_routes):
            return
        self.routes.add(added_route)

        bound_routes = self.get_connected_routes(added_route.first_end, added_route.second_end)
        route_types = {r.type for r in bound_routes}

        if route_types == set(self.get_day_types()) or added_route.type == self.route_type_all:
            for route_type in route_types:
                self.routes.remove(Route(first_end=added_route.first_end, second_end=added_route.second_end, type=route_type))
            self.routes.add(Route(first_end=added_route.first_end, second_end=added_route.second_end, type=self.route_type_all))

    def get_connected_routes(self, first_square: str, second_square: str | None = None) -> set[Route]:
        if second_square is None:
            return {route for route in self.routes if first_square in (route.first_end, route.second_end)}
        return {route for route in self.routes if {route.first_end, route.second_end} == {first_square, second_square}}

    def remove_route(self, route: Route):
        try:
            self.routes.remove(route)
        except KeyError:
            raise RuntimeError("Route not found.")
    
    def filter_routes_of_type(self, route_type: str, routes: set[Route]) -> set[Route]:
        return {route for route in routes if route.type == route_type or route.type == self.route_type_all}
    
    # Route types methods ---------------------------------------------------------------
    def get_route_types(self) -> list[str]:
        return list(self.route_types)

    def get_route_type_all(self) -> str:
        return self.route_type_all

    # Calendar methods ----------------------------------------------------------------------
    def get_calendar(self) -> list[str]:
        return self.calendar
    
    @in_progress("Cannot modify calendar after the game has started.")
    def add_day(self, day: str):
        if day not in self.get_day_types():
            raise RuntimeError("Invalid day type.")
        if len(self.calendar) >= 99:
            raise RuntimeError("Cannot have more than 99 days in the calendar.")
        self.calendar.append(day)
    
    @in_progress("Cannot modify calendar after the game has started.")
    def remove_day(self, day_number: int):
        if 0 < day_number <= len(self.calendar):
            self.calendar = [day for index, day in enumerate(self.calendar) if index + 1 != day_number]
        else:
            raise IndexError("Day number out of range.")
        
    @in_progress("Cannot modify calendar after the game has started.")
    def modify_day(self, day_number: int, new_day_type: str):
        if 0 < day_number <= len(self.calendar):
            self.calendar[day_number - 1] = new_day_type
        else:
            raise IndexError("Day number out of range.")
        
    def get_day_types(self) -> list[str]:
        return [route_type for route_type in self.route_types if route_type != self.route_type_all]

    # Game methods ----------------------------------------------------------------------
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
            raise RuntimeError("Cannot simulate game if game is not started.")
        
        while self.status == GameStatus.IN_PROGRESS:
            if self.current_player is None:
                break
            route_type = self.calendar[self.day_count - 1]
            routes = self.filter_routes_of_type(route_type, routes=self.get_connected_routes(self.current_player.position))
            available_squares = [
                (route.first_end if route.second_end == self.current_player.position else route.second_end)
                for route in routes
            ]
            self.move_player(self.current_player.id, random.choice(available_squares))

    def can_move(self, player: Player) -> bool:
        day_type = self.calendar[self.day_count - 1]
        routes = self.get_connected_routes(player.position)
        
        if player.position == self.castle_square:
            return False
        return len(self.filter_routes_of_type(day_type, routes)) > 0

    def move_player(self, player_id: str, new_position: str):
        if self.status != GameStatus.IN_PROGRESS:
            raise RuntimeError("Cannot move players when the game is not in progress.")
        
        player = self.get_player(player_id)
        if player != self.current_player:
            raise RuntimeError("It's not this player's turn.")
        
        route_type = self.calendar[self.day_count - 1]
        routes = self.filter_routes_of_type(route_type, routes=self.get_connected_routes(player.position, new_position))
        if not routes:
            raise RuntimeError("No valid route between the two squares.")
        
        if player.position == self.castle_square:
            raise RuntimeError("Le joueur est coincé au palais.")

        self.add_to_history(player.id, player.position, new_position)
        player.position = new_position
        self.set_next_current_player()

    def at_new_turn(self):
        self.day_count += 1
        if (
            self.day_count > len(self.calendar) 
            or all(player.position == self.castle_square for player in self.players_dict.values()) 
        ):
            self.at_game_end()

    def at_game_end(self):
        self.status = GameStatus.COMPLETED
        self.day_count = 0
        self.current_player = None
        self.player_iterator = cycle(enumerate([]))

    @in_progress("Game has already started.")
    def start_game(self):        
        if not self.players_dict:
            raise RuntimeError("Cannot start game without players.")
        if not self.calendar:
            raise RuntimeError("Cannot start game without a calendar.") 
        if not self.routes:
            raise RuntimeError("Cannot start game without routes.")
        
        self.status = GameStatus.IN_PROGRESS
        self.game_history = []
        self.player_iterator = cycle(enumerate(self.players_dict.values()))
        self.set_next_current_player()

    def stop_game(self):
        if self.status != GameStatus.IN_PROGRESS:
            raise RuntimeError("Game is not in progress.")
        self.at_game_end()
        self.status = GameStatus.NOT_STARTED
        self.game_history = []

    def set_next_current_player(self):
        ran_once = False
        while (self.current_player is not None) and (not self.can_move(self.current_player)) or not ran_once:
            index, self.current_player = next(self.player_iterator)
            ran_once = True
            if index == 0:
               self.at_new_turn()

    # other methods ----------------------------------------------------------------------
    def export(self) -> ExportData:
        return ExportData(
            version='1.0',
            players=self.get_players(),
            calendar=self.get_calendar(),
            routes=self.get_all_routes(),
            route_type_all=self.get_route_type_all(),
            castle_square=self.get_castle_square(),
            squares=self.get_squares(),
            game_status=self.game_status(),
            game_history=self.game_history
        )
    
    @in_progress("Cannot import game data while the game is being played.")    
    def import_data(self, data: ExportData) -> 'GameModel':
        new_model = GameModel()

        # check data integrity
        squares = self.get_squares()
        new_model.squares = []
    
        for player in data.players:
            if player.position not in squares:
                player.position = data.castle_square
        
        valid_routes = [
            route for route in data.routes
            if (route.first_end in squares 
                and route.second_end in squares
                and route.type in self.route_types)
        ]
        data.routes = valid_routes
        
        if data.castle_square not in squares and data.squares:
            data.castle_square = data.squares[0]
        
        data.calendar = [
            day for day in data.calendar
            if day in self.get_day_types()
        ]
        # apply data to new model
        new_model.route_type_all = data.route_type_all
        new_model.castle_square = data.castle_square

        for square in data.squares:
            new_model.add_square(square)

        for day in data.calendar:
            new_model.add_day(day)

        for player in data.players:
            new_model.add_player(player)
        
        for route in data.routes:
            new_model.add_route(route)

        return new_model