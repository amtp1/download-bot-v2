from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.db import Role
from bot.filters import ChatTypeFilter, RoleCheckFilter
from bot.utils.texts import help_message

# Создание маршрутизатора
router = Router(name="Help Text")

# Регистрация фильтров
router.message.filter(RoleCheckFilter(Role.USER))
router.message.filter(ChatTypeFilter(["private"]))


@router.message(F.text == "Help", flags={"delay": 2})
@router.message(Command("help"), flags={"delay": 2})
async def help_handler(m: Message) -> None:
    return await m.answer(help_message())


# Псевдоним
router_help = router
