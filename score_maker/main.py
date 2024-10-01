from fastapi import FastAPI
from score_maker.app.routers.event_router import router as event_router

app = FastAPI()
app.include_router(event_router)

