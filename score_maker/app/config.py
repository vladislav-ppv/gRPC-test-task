import dotenv
from pydantic import SecretStr
from pydantic_settings import BaseSettings as BaseSettings_, SettingsConfigDict
from sqlalchemy import URL


class BaseSettings(BaseSettings_):
    model_config = SettingsConfigDict(
        env_file=dotenv.find_dotenv(), env_file_encoding="utf-8", extra="ignore"
    )


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


class Settings(
    PostgresSettings,
):
    pass


settings = Settings()
