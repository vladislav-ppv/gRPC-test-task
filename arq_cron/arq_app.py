import asyncio
import logging

from arq import create_pool
from arq.connections import RedisSettings

from src.config import settings


async def main():
    redis = await create_pool(RedisSettings.from_dsn(settings.redis.build_url()))
    await redis.enqueue_job("check_outbox")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("arq").setLevel(logging.INFO)


    async def wrapper():
        await main()
        await asyncio.Event().wait()  # keep the event loop running forever


    asyncio.run(wrapper())
