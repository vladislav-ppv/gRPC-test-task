from enum import Enum

from pydantic import BaseModel, Field


class ScoreStatusEnum(Enum):
    mutable = "mutable"
    immutable = "immutable"


class Score(BaseModel):
    event_id: int
    rate: int = Field(ge=1, le=5)


class ScoreWithStats(Score):
    status: ScoreStatusEnum | None = None


class SetScoreRequest(ScoreWithStats):
    ...
