from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

from line_provider.pb.line_provider_pb2 import StatusEnum as _StatusEnum


# Перевод Protobuf Enum в Python Enum
class StatusEnum(Enum):
    PROCESSING = _StatusEnum.STATUS_PROCESSING
    HIGH_SCORE = _StatusEnum.STATUS_HIGH_SCORE
    LOW_SCORE = _StatusEnum.STATUS_LOW_SCORE


class BaseEvent(BaseModel):
    event_id: int
