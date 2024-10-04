import asyncio
import logging

from arq import create_pool, cron
from arq.connections import RedisSettings
from sqlalchemy import select

from src.config import settings
from src.database.core import async_session
from src.database.models import ScoreOutboxModel


async def main():
    redis = await create_pool(RedisSettings.from_dsn(settings.redis.build_url()))
    await redis.enqueue_job("check_outbox")


async def check_outbox(ctx):
    async with async_session() as session:
        query = select(ScoreOutboxModel).filter_by(processed=False)
        result = await session.execute(query)
        scores: list[ScoreOutboxModel] = result.scalars().all()
        logging.info(scores)

        for score in scores:
            logging.info("MOCK sending task to process_score")
            # app.send_task("process_score", args=(score.event_id, score.rate))

            # Обновляем статус обработки
            score.processed = True
            session.add(score)

        await session.commit()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("arq").setLevel(logging.INFO)

    async def wrapper():
        await main()
        await asyncio.Event().wait()  # keep the event loop running forever


    asyncio.run(wrapper())