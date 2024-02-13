from datetime import datetime as dt

from aiogram import Bot, Router
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.orm import sessionmaker

from bot.config import load_config
from bot.db import Role, SQLUser
from bot.filters import ChatTypeFilter, RoleCheckFilter
from bot.utils import ControlStates

config = load_config("bot.ini")
bot = Bot(config.bot.token, parse_mode="HTML")

# from bot.keyboards.basic import IKB_PROFILE, IKB_START

# Создание маршрутизатора
router = Router(name="Command statistic")

# Регистрация фильтров
router.message.filter(RoleCheckFilter(Role.ADMINISTRATOR))
router.message.filter(ChatTypeFilter(["private"]))


# Регистрация обработчиков
@router.message(Command("mail"), flags={"delay": 2})
async def mailing(
    m: Message,
    command: CommandObject,
    bot: Bot,
    session: sessionmaker,
    state: FSMContext,
) -> None:
    """
    Обработчик, который реагирует на команду /mail
    """

    await m.answer(text="Напишите текст для рассылки:")
    return await state.set_state(ControlStates.waiting_mail)


@router.message(ControlStates.waiting_mail, flags={"delay": 2})
async def mailing_wait(m: Message, session: sessionmaker, state: FSMContext):
    sql_user = SQLUser(session)
    users = await sql_user.all()

    await m.answer("Рассылка началась...")
    start_time = dt.now()

    for user in users:
        try:
            await bot.send_message(chat_id=user.user_id, text=m.text)
        except (TelegramBadRequest, TelegramForbiddenError):
            await sql_user.update(user_id=user.user_id, is_blocked=True)

    end_time = dt.now()
    total_sec = (end_time - start_time).total_seconds()
    await state.clear()
    return await m.answer("Время рассылки: {:.2f} seconds.".format(total_sec))


# Псевдоним
router_mailing = router
