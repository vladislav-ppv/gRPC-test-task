import logging

from arq import Retry

logger = logging.getLogger(__name__)

async def on_job_failure(ctx, job_id, exc):
    if isinstance(exc, Retry):
        logger.error(f"Task {job_id} exceeded retry limit.")
        # TODO: compensation transaction
        # await compensation_transaction_remove_score_grpc(ctx, job_id)
        logger.info(ctx, job_id, exc)

def configure_logging() -> None:
    logging.config.dictConfig(
        {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'console': {
                    'class': 'logging.Formatter',
                    'datefmt': '%H:%M:%S',
                    'format': '%(levelname)s:\t\b%(asctime)s %(name)s:%(lineno)d %(message)s',
                },
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'console',
                },
            },
            'loggers': {
                'arq': {'handlers': ['console'], 'level': 'INFO', 'propagate': True},
            },
        }
    )

async def on_startup(*args, **kwargs):
    configure_logging()
