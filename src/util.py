import enum
import uuid
import pydantic
import typing
import random

class Day(enum.StrEnum):
    LIVRAISON = "Livraison"
    DOLEANCES = "Doléances"
    MARCHANDS = "Marchands"
    LABEUR = "Labeur"

class RouteType(enum.StrEnum):
    LIVRAISON = "Livraison"
    DOLEANCES = "Doléances"
    MARCHANDS = "Marchands"
    LABEUR = "Labeur"
    TOUT = "Tout"

ROUTE_ALL: RouteType = RouteType.TOUT

class Square(enum.StrEnum):
    ENTREPOTS = "Entrepôts royaux"
    ARTISANTS = "Quartier des artisants"
    MARCHANDS = "Quartier des marchands"
    GARDES = "Salle des gardes"
    PALAIS = "Palais"

CASTLE_SQUARE = Square.PALAIS

class GameStatus(enum.StrEnum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"    

def get_random_color() -> str:
    return f"#{random.randint(0, 0xFFFFFF).to_bytes(3).hex().upper()}"

class Route(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(frozen=True)
    first_end: Square
    second_end: Square
    type: RouteType

    def __hash__(self) -> int:
        return hash((tuple(sorted([self.first_end, self.second_end])), self.type))
    
    def __eq__(self, value: object) -> bool:
        if type(value) == Route:
            return hash(self) == hash(value)
        raise NotImplemented
    
class Player(pydantic.BaseModel):
    #model_config = pydantic.ConfigDict(frozen=True)
    id: str = pydantic.Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    position: Square
    color: str = pydantic.Field(default_factory=get_random_color)


class StatusDict(typing.TypedDict):
    status: GameStatus
    day_count: int
    current_player: Player | None
    current_day_type: Day | None

class PlayerDict(typing.TypedDict):
    id: str
    name: str
    color: str
    position: Square

class RouteDict(typing.TypedDict):
    first_end: Square
    second_end: Square
    type: RouteType

class ExportData(typing.TypedDict):
    players: list[PlayerDict]
    calendar: list[Day]
    routes: list[RouteDict]
    route_types: list[RouteType]
    route_type_all: RouteType
    route_colors: dict[RouteType, str]
    game_state: StatusDict

class ExportDict(typing.TypedDict):
    version: str
    data: ExportData

class GameHistoryEntry(typing.TypedDict):
    day_type: Day
    moves: list[tuple[str, str, str]]  # List of (player_id, from_square, to_square)
