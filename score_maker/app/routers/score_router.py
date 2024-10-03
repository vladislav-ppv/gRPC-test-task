from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from score_maker.app.dependencies.database import get_db
from score_maker.app.dependencies.grpc.event import get_events_grpc
from score_maker.app.schemas.event import EventResponse
from score_maker.app.schemas.score import Score
from score_maker.app.database.repository import ScoreRepository

router = APIRouter()


@router.get("/events")
async def get_events() -> list[EventResponse]:
    return await get_events_grpc()


@router.post("/set-score")
async def set_score(score: Score, session: Annotated[AsyncSession, Depends(get_db)]):
    repo = ScoreRepository(session=session)
    await repo.insert(score)
    await repo.outbox_insert(score)
    await repo.commit()

@router.get("/scores", response_model_exclude={"status"})
async def get_scores() -> list[Score]:
    ...
