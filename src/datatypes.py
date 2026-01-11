import enum
import uuid
import pydantic
import typing

class Day(enum.StrEnum):
    LIVRAISON = "livraison"
    DOLEANCES = "doleances"
    MARCHANDS = "marchands"
    LABEUR = "labeur"

class RouteType(enum.StrEnum):
    LIVRAISON = "livraison"
    DOLEANCES = "doleances"
    MARCHANDS = "marchands"
    LABEUR = "labeur"
    TOUT = "tout"

class Square(enum.StrEnum):
    ENTREPOTS = "entrepots_royaux"
    ARTISANTS = "quartier_artisants"
    MARCHANDS = "quartier_marchands"
    GARDES = "salle_gardes"
    PALAIS = "palais"
    NONE = "none"

class GameStatus(enum.StrEnum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"    

class Route(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(frozen=True)
    first_end: Square
    second_end: Square
    type: RouteType

    def __hash__(self) -> int:
        return hash((self.first_end, self.second_end, self.type))
    
class Player(pydantic.BaseModel):
    #model_config = pydantic.ConfigDict(frozen=True)
    id: uuid.UUID = pydantic.Field(default_factory=lambda: uuid.uuid4())
    name: str = ""
    position: Square = Square.NONE

    def __hash__(self) -> int:
        return hash(self.id.int)

void_player = Player(name="Void Player")

class StatusDict(typing.TypedDict):
    status: GameStatus
    day_count: int
    current_player: Player
    current_day_type: Day | None
