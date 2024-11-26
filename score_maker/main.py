from contextlib import asynccontextmanager

from fastapi import FastAPI

from score_maker.app.database.core import engine
from score_maker.app.database.models import Base
from score_maker.app.routers.score_router import router as event_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting database...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(event_router)
