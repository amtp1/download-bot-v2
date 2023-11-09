from datetime import datetime as dt
from enum import IntEnum

from sqlalchemy import (BigInteger, Column, DateTime, String, Boolean, Enum)

from .base import Base


class Role(IntEnum):
    USER = 0
    MODERATOR = 1
    ADMINISTRATOR = 2


class UserModel(Base):
    """
    Основная модель пользователей
    """

    __tablename__ = "users"

    id = Column(
        BigInteger, nullable=False, primary_key=True
    )  # Unique id
    role = Column(Enum(Role), default=Role.USER)  # Роль пользователя в проекте
    user_id = Column(BigInteger())
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    download_count = Column(String, nullable=True)
    updated = Column(
        DateTime, default=dt.today(), onupdate=dt.today()
    )  # Date updated of user
    created = Column(
        DateTime(), default=dt.today(), onupdate=dt.today()
    )  # Date created of user
    is_blocked = Column(Boolean(), default=False)

    def __str__(self):
        return f"User Id: {self.user_id}"


class Download(Base):
    """
    Основная модель загрузок
    """

    __tablename__ = "downloads"

    id = Column(
        BigInteger, nullable=False, primary_key=True
    )  # Unique id
    user_id = Column(BigInteger())
    link = Column(String)
    content_type = Column(String)
    service = Column(String)
    created = Column(
        DateTime(), default=dt.today(), onupdate=dt.today()
    )

    def __str__(self):
        return f"Download Id: {self.id}"
