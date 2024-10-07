from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StatusEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STATUS_PROCESSING: _ClassVar[StatusEnum]
    STATUS_LOW_SCORE: _ClassVar[StatusEnum]
    STATUS_HIGH_SCORE: _ClassVar[StatusEnum]
STATUS_PROCESSING: StatusEnum
STATUS_LOW_SCORE: StatusEnum
STATUS_HIGH_SCORE: StatusEnum

class Event(_message.Message):
    __slots__ = ("event_id", "deadline", "status")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    DEADLINE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    event_id: int
    deadline: _timestamp_pb2.Timestamp
    status: StatusEnum
    def __init__(self, event_id: _Optional[int] = ..., deadline: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., status: _Optional[_Union[StatusEnum, str]] = ...) -> None: ...

class GetEventsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetEventsResponse(_message.Message):
    __slots__ = ("events",)
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[Event]
    def __init__(self, events: _Optional[_Iterable[_Union[Event, _Mapping]]] = ...) -> None: ...

class UpdateEventStatusByScoreRequest(_message.Message):
    __slots__ = ("event_id", "score")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    event_id: int
    score: int
    def __init__(self, event_id: _Optional[int] = ..., score: _Optional[int] = ...) -> None: ...

class UpdateEventStatusByScoreResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
