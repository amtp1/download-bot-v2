from aiogram import Bot, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from sqlalchemy.orm import sessionmaker

from bot.db import Role, SQLDownload, SQLUser
from bot.filters import ChatTypeFilter, RoleCheckFilter
from bot.utils.texts import statistic_message

# Создание маршрутизатора
router = Router(name="Command statistic")

# Регистрация фильтров
router.message.filter(RoleCheckFilter(Role.ADMINISTRATOR))
router.message.filter(ChatTypeFilter(["private"]))


@router.message(Command("stat"), flags={"delay": 2})
async def statistic(
    m: Message, command: CommandObject, bot: Bot, session: sessionmaker
) -> None:
    """
    Обработчик, который реагирует на команду /statistic
    """
    sql_user = SQLUser(session)
    sql_download = SQLDownload(session)

    users = await sql_user.all()
    blocked_users = await sql_user.blocked_users()
    downloads = await sql_download.all()
    users_week = await sql_user.get_users_in_week()

    users_total = len(users)
    users_blocked = len(blocked_users)
    users_active = users_total - users_blocked

    return await m.answer(
        statistic_message(
            users_total=users_total,
            users_blocked=users_blocked,
            users_active=users_active,
            users_week=len(users_week),
            downloads_total=len(downloads),
        )
    )


# Псевдоним
router_statistic = router
