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

class ExportDict(typing.TypedDict):
    version: str
    players: list[Player]
    calendar: list[str]
    routes: list[Route]
    route_types: list[str]
    route_type_all: str
    route_colors: dict[str, str]
    game_status: StatusDict
    castle_square: str
    game_history: list[GameHistoryEntry]
    squares: list[str]
