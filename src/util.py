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

ROUTE_ALL: str = RouteType.TOUT

class Square(enum.StrEnum):
    ENTREPOTS = "Entrepôts royaux"
    ARTISANTS = "Quartier des artisants"
    MARCHANDS = "Quartier des marchands"
    GARDES = "Salle des gardes"
    PALAIS = "Palais"

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
        return hash((self.first_end, self.second_end, self.type))
    
class Player(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(frozen=True)
    id: uuid.UUID = pydantic.Field(default_factory=lambda: uuid.uuid4())
    name: str = ""
    position: Square | None = None
    color: str = pydantic.Field(default_factory=get_random_color)

void_player = Player(name="Void Player")

class StatusDict(typing.TypedDict):
    status: GameStatus
    day_count: int
    current_player: Player
    current_day_type: Day | None


