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
    game_status: StatusDict | None
    castle_square: str = "Palais"
    game_history: list[GameHistoryEntry] | None
    squares: list[str] = pydantic.Field(default_factory=lambda: [])



