from sqlalchemy.ext.asyncio import AsyncSession

from score_maker.app.schemas.score import Score
from score_maker.app.database.models import ScoreModel


class ScoreRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def insert(self, score: Score):
        async with self.session as session:
            score_model = ScoreModel(**score.model_dump())
            self.session.add(score_model)
            await session.commit()
