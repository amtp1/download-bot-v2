from aiogram import Bot, Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import Message
from sqlalchemy.orm import sessionmaker

from bot.db import Role
from bot.filters import ChatTypeFilter, RoleCheckFilter
from bot.keyboards import KB_START
from bot.utils.texts import welcome_message

# Создание маршрутизатора
router = Router(name="Command start")

# Регистрация фильтров
router.message.filter(RoleCheckFilter(Role.USER))
router.message.filter(ChatTypeFilter(["private"]))


@router.message(CommandStart(), flags={"delay": 2})
async def start(
    m: Message, command: CommandObject, bot: Bot, session: sessionmaker
) -> None:
    """
    Обработчик, который реагирует на команду /start
    """
    return await m.answer(
        welcome_message(m.from_user.first_name if m.from_user else None),
        reply_markup=KB_START,
    )


# Псевдоним
router_start = router
