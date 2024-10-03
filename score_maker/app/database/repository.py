from sqlalchemy.ext.asyncio import AsyncSession

from score_maker.app.database.models import ScoreModel, ScoreOutboxModel
from score_maker.app.schemas.score import Score


class ScoreRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def insert(self, score: Score):
        score_model = ScoreModel(**score.model_dump())
        self.session.add(score_model)

    async def outbox_insert(self, score: Score):
        outbox_model = ScoreOutboxModel(**score.model_dump())
        self.session.add(outbox_model)

    async def commit(self):
        await self.session.commit()
