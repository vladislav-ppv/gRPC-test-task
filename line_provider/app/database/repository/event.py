from sqlalchemy import select, update, Result
from sqlalchemy.ext.asyncio import AsyncSession

from line_provider.app.database.models import EventModel
from line_provider.app.schemas.event import EventWithDeadlineAndStatus, StatusEnum
from line_provider.app.services.utils import calculate_status_by_score


class EventRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = EventModel

    async def insert(self, score: EventWithDeadlineAndStatus):
        event_model = self.model(**score.model_dump())
        self.session.add(event_model)

    async def get(self, **filter_by) -> Result | None:
        result = await self.session.execute(
            select(self.model).filter_by(**filter_by)
        )
        return result

    async def update(self, filters: dict, values: dict):
        await self.session.execute(
            update(self.model)
            .filter_by(**filters)
            .values(**values)
        )

    async def get_all_events(self) -> list[EventModel]:
        result = await self.get()
        events: list[EventModel] = result.scalars().all()
        return events

    async def update_event_status_by_score(self, event_id: int, score: int):
        status: StatusEnum = calculate_status_by_score(score)
        await self.update({"id": event_id}, {"status": status.name})

    async def commit(self):
        await self.session.commit()
