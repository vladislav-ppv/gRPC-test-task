import logging

from line_provider.app.database.core import SessionLocal
from line_provider.app.database.models import EventModel
from line_provider.app.database.repository.event import EventRepository
from line_provider.app.services.exceptions import ScoreIsNotBetween1And5
from line_provider.pb.line_provider_pb2 import GetEventsResponse, GetEventsRequest, Event, \
    UpdateEventStatusByScoreRequest, UpdateEventStatusByScoreResponse
from line_provider.pb.line_provider_pb2_grpc import EventServiceServicer


class BaseEventServicer(EventServiceServicer):
    async def GetEvents(self, request: GetEventsRequest, context):
        """Fetch events from database and format them to the gRPC response model"""
        async with SessionLocal() as session:
            repo = EventRepository(session=session)
            event_models: list[EventModel] = await repo.get_all_events()
            event_models_for_response: list[Event | None] = []

            for event in event_models:
                event_models_for_response.append(
                    Event(event_id=event.id, deadline=event.deadline, status=event.status.value))

        return GetEventsResponse(events=events)
        return GetEventsResponse(events=event_models_for_response)

