import logging

import redis
from arq import cron, Retry
from arq.connections import RedisSettings
from celery import Celery
from sqlalchemy import select

from src.database.core import async_session
from src.database.models import ScoreOutboxModel
from src.config import settings

logger = logging.getLogger(__name__)
redis_client = redis.Redis(host='localhost', port=6379, db=0)


async def process_score(ctx, event_id: int, rate: int):
    """
    Process a score for a given event_id.

    Acquires a lock based on the event_id to prevent multiple tasks from running at the same time.
    If the lock is not acquired, the task is skipped.

    The task performs some score processing logic and updates the status in the database.
    Finally, the lock is released.

    :param self: The Celery task instance.
    :param event_id: The event ID to process.
    :param rate: The rate to process .
    """

    # Acquire lock
    lock_key = f"lock:{event_id}"

    lock_acquired = redis_client.setnx(lock_key, 1)  # returns 1 if lock acquired successfully
    if not lock_acquired:
        logger.info(f"Task for event_id {event_id} is already running. Skipping.")
        return

    try:
        logging.info("MOCK gRPC request with processing score")

        # Update status in the database
        async with async_session() as session:
            query = session.query(ScoreOutboxModel).filter_by(event_id=event_id)
            result = await session.execute(query)

            score: list[ScoreOutboxModel] = result.scalars().first()
            score.processed = True
            session.add(score)

            await session.commit()

    except Exception as e:
        logger.error(f"An error occurred while processing score for event_id {event_id}. Retrying.", exc_info=e)
        raise Retry(defer=ctx['job_try'] * 5)

    finally:
        # Release lock
        await redis_client.delete(lock_key)


async def check_outbox(ctx):
    async with async_session() as session:
        query = select(ScoreOutboxModel).filter_by(processed=False)
        result = await session.execute(query)
        scores: list[ScoreOutboxModel] = result.scalars().all()
        logging.info(scores)

        for score in scores:
            # Отправляем задачу на обработку в Worker
            logging.info("MOCK sending task to process_score")
            # app.send_task("process_score", args=(score.event_id, score.rate))

            # Обновляем статус обработки
            score.processed = True
            session.add(score)

        await session.commit()


class WorkerSettings:
    functions = [check_outbox, process_score]
    redis_settings: RedisSettings = RedisSettings()
    cron_jobs = [
        cron(check_outbox, name="Check outbox table every 5 seconds", second=5)
    ]
