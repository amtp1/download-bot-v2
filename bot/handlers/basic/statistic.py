from aiogram import Bot, Router
from aiogram.filters import CommandObject, Command
from aiogram.types import Message
from sqlalchemy.orm import sessionmaker

from bot.db import Role, SQLUser, SQLDownload
from bot.filters import ChatTypeFilter, RoleCheckFilter

# from bot.keyboards.basic import IKB_PROFILE, IKB_START

# Создание маршрутизатора
router = Router(name="Command statistic")

# Регистрация фильтров
router.message.filter(RoleCheckFilter(Role.ADMINISTRATOR))
router.message.filter(ChatTypeFilter(["private"]))


# Регистрация обработчиков
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
    text = (
        f"👤Users\n"
        f"➜ All: {len(users)}\n"
        f"\t\t\t\t➜ Blocked: {len(blocked_users)}\n\n"
        f"💾Downloads\n"
        f"➜ All: {len(downloads)}"
    )
    return await m.answer(text=text)


# Псевдоним
router_statistic = router
