from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.orm import sessionmaker

from bot.db import Role
from bot.filters import ChatTypeFilter, RoleCheckFilter

# from bot.keyboards.basic import IKB_PROFILE, IKB_START

# Создание маршрутизатора
router = Router(name="Help Text")

# Регистрация фильтров
router.message.filter(RoleCheckFilter(Role.USER))
router.message.filter(ChatTypeFilter(["private"]))


# Регистрация обработчиков
@router.message(F.text == 'Help', flags={"delay": 2})
async def help(m: Message):
    return await m.answer('Downloader Bot')


# Псевдоним
router_help = router
