import logging

import redis
from celery import Celery
from celery.utils.log import get_task_logger

from src.database.core import async_session
from src.database.models import ScoreOutboxModel
from src.config import settings

logger = get_task_logger(__name__)
app = Celery('outbox_checker', broker=settings.celery_settings.build_celery_broker_url(),
             backend=settings.celery_settings.build_celery_backend_url())
redis_client = redis.Redis(host='localhost', port=6379, db=0)


@app.task(bind=True, max_retries=5)
async def process_score(self, event_id: int, rate: int):
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
        raise self.retry(exc=e, countdown=10)

    finally:
        # Release lock
        await redis_client.delete(lock_key)


@app.task
async def check_outbox():
    async with async_session() as session:
        query = session.query(ScoreOutboxModel).filter_by(processed=False)
        result = await session.execute(query)
        scores: list[ScoreOutboxModel] = result.scalars().all()
        logging.info(scores)

        for score in scores:
            # Отправляем задачу на обработку в Worker
            app.send_task("process_score", args=(score.event_id, score.rate))

            # Обновляем статус обработки
            score.processed = True
            session.add(score)

        await session.commit()