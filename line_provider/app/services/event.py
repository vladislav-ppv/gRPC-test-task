import datetime

from line_provider.pb.line_provider_pb2_grpc import EventServiceServicer
from line_provider.pb.line_provider_pb2 import GetEventsResponse, Event, StatusEnum


class BaseEventServicer(EventServiceServicer):
    def GetEvents(self, request, context):
        # Логика для получения доступных событий
        events = []
        for i in range(5):
            events.append(Event(event_id=i, deadline=datetime.datetime.now(), status=StatusEnum.STATUS_PROCESSING))
        print(f"Getting events {request}")

        return GetEventsResponse(events=events)
