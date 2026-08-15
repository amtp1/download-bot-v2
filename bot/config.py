import configparser
from dataclasses import dataclass
from pathlib import Path

from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool


@dataclass
class BotConfig:
    token: str
    admin_id: int


@dataclass
class DBConfig:
    path: str

    def create_url(self) -> str:
        db_path = Path(self.path).resolve().as_posix()
        return f"sqlite+aiosqlite:///{db_path}"

    def create_engine(self) -> AsyncEngine:
        return create_async_engine(
            url=self.create_url(),
            echo=False,
            poolclass=NullPool,
        )

    def create_session(self) -> sessionmaker:
        return sessionmaker(
            bind=self.create_engine(), class_=AsyncSession, expire_on_commit=False
        )


@dataclass
class RedisConfig:
    host: str
    username: str
    password: str

    def connect(self):
        return Redis(host=self.host, username=self.username, password=self.password)


@dataclass
class Rapid:
    youtube_token: str
    tiktok_token: str


@dataclass
class Config:
    bot: BotConfig
    db: DBConfig
    redis: RedisConfig
    rapid: Rapid


def load_config(path: str):
    """
    Загрузка конфигурации
    :param path: Путь к файлу конфигурации
    """
    file_config = configparser.ConfigParser()
    file_config.read(path)
    return Config(
        bot=BotConfig(**file_config["bot"]),
        db=DBConfig(**file_config["db"]),
        redis=RedisConfig(**file_config["redis"]),
        rapid=Rapid(**file_config["rapid"]),
    )
