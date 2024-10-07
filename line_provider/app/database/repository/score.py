from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession

from line_provider.app.schemas.score import Score
from line_provider.app.database.models import ScoreModel


class ScoreRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = ScoreModel

    async def insert(self, score: Score):
        async with self.session as session:
            score_model = self.model(**score.model_dump())
            session.add(score_model)

    async def update(self, filters: dict, values: dict):
        async with self.session as session:
            await session.execute(
                update(self.model)
                .filter_by(**filters)
                .values(**values)
            )

    async def get(self, **filter_by):
        async with self.session as session:
            result = await session.execute(
                select(self.model).filter_by(**filter_by)
            )
            return result.scalars().first()

    async def commit(self):
        await self.session.commit()
