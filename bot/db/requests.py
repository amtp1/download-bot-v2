from datetime import datetime, timedelta

from sqlalchemy import select, update
from sqlalchemy.orm import sessionmaker

from bot.db import Role, UserModel, Download


class SQLUser:
    def __init__(self, session: sessionmaker):
        """
        Метод инициализации
        :param session: Пул соединений с БД
        :return: bool
        """
        self.session = session

    async def is_exists(self, user_id: int) -> bool:
        """
        Существует ли пользователь
        :param user_id: Телеграм id пользователя
        :return: bool
        """
        async with self.session() as session:
            async with session.begin():
                return (
                    await session.execute(
                        select(UserModel).where(UserModel.user_id == user_id)
                    )
                ).first()

    async def add(self, user_id: int, first_name: str, last_name: str) -> None:
        """
        Добавить нового пользователя
        :param user_id: Телеграм id пользователя
        :param full_name: Полное имя пользователя
        :return: None
        """
        async with self.session() as session:
            async with session.begin():
                user = UserModel(id=user_id, first_name=first_name, last_name=last_name)
                session.add(user)

    async def get(self, user_id: int) -> UserModel:
        """
        Получить данные пользователя
        :param user_id: Телеграм id пользователя
        :return: UserModel
        """
        async with self.session() as session:
            async with session.begin():
                return (
                    (
                        await session.execute(
                            select(UserModel).where(UserModel.user_id == user_id)
                        )
                    )
                    .scalars()
                    .first()
                )

    async def get_by_role(self, role: Role):
        """
        Получить пользователей по роли
        :param role: Роль пользователей
        :return: UserModel
        """
        async with self.session() as session:
            async with session.begin():
                return (
                    await session.execute(
                        select(UserModel).where(UserModel.role == role)
                    )
                ).scalars()

    async def update(self, user_id: int, **kwargs) -> None:
        """
        Обновить данные пользователя
        :param user_id: Телеграм id пользователя
        :param kwargs: Параметры которые нужно обновить
        :return: None
        """
        async with self.session() as session:
            async with session.begin():
                await session.execute(
                    update(UserModel).where(UserModel.id == user_id).values(kwargs)
                )

    async def get_users_in_week(self) -> list[datetime]:
        """
        Получить дату регистрации новых пользователей за неделю
        :return: list[datetime]
        """
        async with self.session() as session:
            async with session.begin():
                week = datetime.today() - timedelta(days=7)
                return list(
                    (
                        await session.execute(
                            select(UserModel.created).where(
                                UserModel.created >= week
                            )
                        )
                    ).scalars()
                )

    async def blocked_users(self):
        async with self.session() as session:
            async with session.begin():
                return list(
                    (
                        await session.execute(
                            select(UserModel).where(
                                UserModel.is_blocked == True
                            )
                        )
                    ).scalars()
                )

    async def all(self):
        async with self.session() as session:
            async with session.begin():
                return list(
                    (
                        await session.execute(
                            select(UserModel)
                        )
                    ).scalars()
                )


class SQLDownload:
    def __init__(self, session: sessionmaker):
        """
        Метод инициализации
        :param session: Пул соединений с БД
        :return: bool
        """
        self.session = session

    async def add(self, user_id: int, link: str, content_type: str, service: str) -> None:
        """
        Добавить нового пользователя
        :param user_id: Телеграм id пользователя
        :return: None
        """
        async with self.session() as session:
            async with session.begin():
                downlod = Download(user_id=user_id, link=link, content_type=content_type, service=service)
                session.add(downlod)

    async def all(self):
        async with self.session() as session:
            async with session.begin():
                return list(
                    (
                        await session.execute(
                            select(Download)
                        )
                    ).scalars()
                )
