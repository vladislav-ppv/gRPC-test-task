import logging

from celery import Celery

from src.database.core import async_session
from src.database.models import ScoreOutboxModel
from src.config import settings

app = Celery('outbox_checker', broker=settings.celery_settings.build_celery_broker_url(),
             backend=settings.celery_settings.build_celery_backend_url())


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Запускаем проверку Outbox каждую секунду
    sender.add_periodic_task(1.0, check_outbox.s(), name='Check outbox every second')


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
