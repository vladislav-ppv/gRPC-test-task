from sqlalchemy.ext.asyncio import AsyncSession

from score_maker.app.database.core import SessionLocal


async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
