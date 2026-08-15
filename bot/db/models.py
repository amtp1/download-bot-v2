from datetime import datetime as dt
from enum import IntEnum

from sqlalchemy import BigInteger, Boolean, Column, DateTime, Enum, String, TypeDecorator

from .base import Base


class FlexibleDateTime(TypeDecorator):
    """SQLite stores datetimes as strings; PG dumps often have uneven microseconds.

    Must bypass DateTime.result_processor — it crashes on values like '.77554'
    before process_result_value() can run.
    """

    impl = DateTime
    cache_ok = True

    @staticmethod
    def _parse(value):
        if value is None or isinstance(value, dt):
            return value

        text = value.replace("T", " ").strip()
        if "." in text:
            head, frac = text.rsplit(".", 1)
            frac = "".join(ch for ch in frac if ch.isdigit())
            frac = (frac + "000000")[:6]
            text = "{}.{}".format(head, frac)
        return dt.fromisoformat(text)

    def process_bind_param(self, value, dialect):
        if value is None or isinstance(value, str):
            return value
        if isinstance(value, dt):
            return value.isoformat(sep=" ", timespec="microseconds")
        return value

    def process_result_value(self, value, dialect):
        return self._parse(value)

    def result_processor(self, dialect, coltype):
        def process(value):
            return self._parse(value)

        return process

    def bind_processor(self, dialect):
        def process(value):
            return self.process_bind_param(value, dialect)

        return process


class Role(IntEnum):
    USER = 0
    MODERATOR = 1
    ADMINISTRATOR = 2


class UserModel(Base):
    """
    Основная модель пользователей
    """

    __tablename__ = "users"

    id = Column(BigInteger, nullable=False, primary_key=True)  # Unique id
    role = Column(
        Enum(
            Role,
            values_callable=lambda enum: [item.name for item in enum],
            native_enum=False,
        ),
        default=Role.USER,
    )  # Роль пользователя в проекте
    user_id = Column(BigInteger())
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    download_count = Column(String, nullable=True)
    updated = Column(
        FlexibleDateTime, default=dt.today(), onupdate=dt.today()
    )  # Date updated of user
    created = Column(
        FlexibleDateTime(), default=dt.today(), onupdate=dt.today()
    )  # Date created of user
    is_blocked = Column(Boolean(), default=False)

    def __str__(self):
        return "User Id: {}".format(self.user_id)


class Download(Base):
    """
    Основная модель загрузок
    """

    __tablename__ = "downloads"

    id = Column(BigInteger, nullable=False, primary_key=True)  # Unique id
    user_id = Column(BigInteger())
    link = Column(String)
    content_type = Column(String)
    service = Column(String)
    created = Column(FlexibleDateTime(), default=dt.today(), onupdate=dt.today())

    def __str__(self):
        return "Download Id: {}".format(self.id)
