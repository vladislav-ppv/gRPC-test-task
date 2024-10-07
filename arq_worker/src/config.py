import dotenv
from pydantic import SecretStr
from pydantic_settings import BaseSettings as BaseSettings_, SettingsConfigDict
from sqlalchemy import URL


class BaseSettings(BaseSettings_):
    model_config = SettingsConfigDict(
        env_file=dotenv.find_dotenv(), env_file_encoding="utf-8", extra="ignore"
    )


class ArqSettings(BaseSettings, env_prefix="CRON_"):
    CHECK_OUTBOX_SECONDS_INTERVAL: int


class CelerySettings(BaseSettings):
    @staticmethod
    def build_celery_broker_url() -> str:
        return settings.redis.build_url()

    @staticmethod
    def build_celery_backend_url() -> str:
        return settings.redis.build_url()


class RedisSettings(BaseSettings, env_prefix="REDIS_"):
    HOST: str
    PORT: int
    DB: str

    def build_url(self) -> str:
        return f"redis://{self.HOST}:{self.PORT}/{self.DB}"


class PostgresSettings(BaseSettings, env_prefix="POSTGRES_"):
    USER: str
    PASSWORD: SecretStr
    HOST: str
    PORT: int
    DB: str

    def build_url(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            host=self.HOST,
            username=self.USER,
            password=self.PASSWORD.get_secret_value(),
            database=self.DB,
            port=self.PORT,
        )


class Settings(BaseSettings):
    postgres: PostgresSettings = PostgresSettings()
    redis: RedisSettings = RedisSettings()
    celery_settings: CelerySettings = CelerySettings()
    arq_settings: ArqSettings = ArqSettings()


settings = Settings()
