from fastapi import APIRouter
from pydantic import BaseModel

from score_maker.app.dependencies.grpc.event import get_events_grpc

router = APIRouter()

@router.get("/events")
async def get_events():
    events = await get_events_grpc()
    print(events)
    return events

