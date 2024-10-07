import logging

from redis.asyncio.client import Redis
from arq import cron, Retry
from arq.connections import RedisSettings, create_pool
from sqlalchemy import select

from arq_worker.src.dependencies.grpc.score import process_score_grpc
from arq_worker.src.services.exceptions import UpdateEventByScoreResponseIsNotSuccess
from src.database.core import async_session
from src.database.models import ScoreOutboxModel
from src.config import settings
from arq_worker.src.services.utils import on_job_failure, on_startup

logger = logging.getLogger(__name__)
redis_client: Redis = Redis.from_url(settings.redis.build_url())


async def process_score(ctx, event_id: int, rate: int):
    """
    Process a score for a given event_id.

    Acquires a lock based on the event_id to prevent multiple tasks from running at the same time.
    If the lock is not acquired, the task is skipped.

    The task performs some score processing logic and updates the status in the database.
    Finally, the lock is released.

    :param ctx: The Arq context.
    :param event_id: The event ID to process.
    :param rate: The rate to process .
    """

    # Acquire lock
    lock_key = f"lock:{event_id}"

    lock_acquired = await redis_client.setnx(lock_key, 1)  # returns 1 if lock acquired successfully
    if not lock_acquired:
        logger.info(f"Task for event_id {event_id} is already running. Skipping.")
        return

    try:
        success: bool = await process_score_grpc(event_id, rate)
        if not success:
            raise UpdateEventByScoreResponseIsNotSuccess("Response from server is not successful")

        # Update status in the database
        async with async_session() as session:
            query = select(ScoreOutboxModel).filter_by(event_id=event_id)
            result = await session.execute(query)

            score: list[ScoreOutboxModel] = result.scalars().first()
            session.add(score)

            await session.commit()

    except Exception as e:
        logger.error(f"An error occurred while processing score for event_id {event_id}. Retrying.", exc_info=e)
        raise Retry(defer=ctx['job_try'] * 5)

    finally:
        # Release lock
        await redis_client.delete(lock_key)


async def check_outbox(ctx):
    arq_redis = await create_pool(RedisSettings.from_dsn(settings.redis.build_url()))

    async with async_session() as session:
        query = select(ScoreOutboxModel).filter_by(processed=False)
        result = await session.execute(query)
        scores: list[ScoreOutboxModel] = result.scalars().all()
        logging.info(scores)

        for score in scores:
            # Send task to Arq Worker
            await arq_redis.enqueue_job("process_score", score.event_id, score.rate)

            score.processed = True
            session.add(score)

        await session.commit()


class WorkerSettings:
    functions = [check_outbox, process_score]
    redis_settings: RedisSettings = RedisSettings.from_dsn(settings.redis.build_url())
    cron_jobs = [
        cron(check_outbox,
             name=f"Check outbox table every {settings.arq_settings.CHECK_OUTBOX_SECONDS_INTERVAL} seconds",
             second=settings.arq_settings.CHECK_OUTBOX_SECONDS_INTERVAL)
    ]
    on_startup = on_startup
    on_job_failure = on_job_failure
