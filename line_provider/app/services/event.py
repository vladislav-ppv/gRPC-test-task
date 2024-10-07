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

        return GetEventsResponse(events=event_models_for_response)

    async def UpdateEventStatusByScore(self, request: UpdateEventStatusByScoreRequest, context):
        """Receive gRPC request and update EventModel by score, provided as a request param"""
        async with SessionLocal() as session:
            repo = EventRepository(session=session)
            try:
                await repo.update_event_status_by_score(event_id=request.event_id, score=request.score)
                await repo.commit()
            except ScoreIsNotBetween1And5:
                logging.error(f"The score is not between 1 and 5. {request.event_id=}")
                return UpdateEventStatusByScoreResponse(success=False)

        return UpdateEventStatusByScoreResponse(success=True)
