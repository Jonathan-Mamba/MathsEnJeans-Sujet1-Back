import enum
import uuid
import pydantic
import typing
import random
import re


class GameStatus(enum.StrEnum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"    


def get_random_color() -> str:
    return f"#{random.randint(0, 0xFFFFFF).to_bytes(3).hex().upper()}"


def is_valid_hex_color(s: str) -> bool:
    return bool(re.fullmatch(r"#[0-9A-Fa-f]{6}", s))


class Route(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(frozen=True)
    first_end: str
    second_end: str
    type: str

    def __hash__(self) -> int:
        return hash((":::".join(sorted([self.first_end, self.second_end])), self.type))
    
    def __eq__(self, value: object) -> bool:
        if type(value) == Route:
            return hash(self) == hash(value)
        return NotImplemented


class Player(pydantic.BaseModel):
    id: str = pydantic.Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    position: str
    color: str = pydantic.Field(default_factory=get_random_color)


class StatusDict(typing.TypedDict):
    status: GameStatus
    day_count: int
    current_player: Player | None
    current_day_type: str | None 


class GameHistoryEntry(typing.TypedDict):
    day_type: str
    moves: list[tuple[str, str, str]]  # List of (player_id, from_square, to_square)


class ExportData(pydantic.BaseModel):
    version: str = "1.0"
    players: list[Player] = pydantic.Field(default_factory=lambda: [])
    calendar: list[str] = pydantic.Field(default_factory=lambda: [])
    routes: list[Route] = pydantic.Field(default_factory=lambda: [])
    route_type_all: str = "Tout"
    route_colors: dict[str, str] = pydantic.Field(default_factory=lambda: {})
    game_status: StatusDict = pydantic.Field(default_factory=lambda: StatusDict(status=GameStatus.NOT_STARTED, day_count=0, current_player=None, current_day_type=None))
    castle_square: str = "Palais"
    game_history: list[GameHistoryEntry] = pydantic.Field(default_factory=lambda: [])
    squares: list[str] = pydantic.Field(default_factory=lambda: [])


def normalize_export_dict(export_data: ExportData) -> ExportData:
    """
    Normalizes an ExportData object by fixing logical inconsistencies.
    Type validation and defaults are handled by Pydantic.
    
    Args:
        export_data: Dictionary or ExportData object to normalize
        
    Returns:
        A corrected ExportData with logical fixes applied
    """
    
    squares_set = set(export_data.squares)
    
    # Fix player positions if invalid
    for player in export_data.players:
        if player.position not in squares_set:
            player.position = export_data.castle_square
        if not is_valid_hex_color(player.color):
            player.color = get_random_color()
    
    # Fix route endpoints - remove routes with invalid endpoints
    valid_routes = [
        route for route in export_data.routes
        if (route.first_end in squares_set 
            and route.second_end in squares_set
            and route.type in export_data.route_colors.keys())
    ]
    export_data.routes = valid_routes
    
    # Fix castle square if not in squares
    if export_data.castle_square not in squares_set and export_data.squares:
        export_data.castle_square = export_data.squares[0]
    
    # Fix calendar - remove types that don't have route colors
    valid_day_types = set(export_data.route_colors.keys()) - {export_data.route_type_all}
    export_data.calendar = [
        day for day in export_data.calendar
        if day in valid_day_types or day == export_data.route_type_all
    ]

    for route_type, color in export_data.route_colors.items():
        if not is_valid_hex_color(color):
            export_data.route_colors[route_type] = get_random_color()
    
    return export_data


