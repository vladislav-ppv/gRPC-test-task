from fastapi import APIRouter

from score_maker.app.dependencies.grpc.event import get_events_grpc
from score_maker.app.schemas.event import EventResponse
from score_maker.app.schemas.score import Score, SetScoreRequest

router = APIRouter()


@router.get("/events")
async def get_events() -> list[EventResponse]:
    return await get_events_grpc()


@router.post("/set-score")
async def set_score(event: Score):
    ...


@router.get("/scores", response_model_exclude={"status"})
async def get_scores() -> list[Score]:
    ...
