from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from score_maker.app.config import settings

DATABASE_URL = settings.build_url()

# Создание базы данных и базового класса для моделей
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
