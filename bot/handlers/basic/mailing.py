from datetime import datetime as dt

from pydantic import ValidationError

from aiogram import Bot, Router
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.orm import sessionmaker

from bot.db import Role, SQLUser
from bot.filters import ChatTypeFilter, RoleCheckFilter
from bot.utils import ControlStates
from bot.utils.texts import (
    mailing_cancelled,
    mailing_prompt,
    mailing_report,
    mailing_started,
)

# Создание маршрутизатора
router = Router(name="Command mailing")

# Регистрация фильтров
router.message.filter(RoleCheckFilter(Role.ADMINISTRATOR))
router.message.filter(ChatTypeFilter(["private"]))


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
    await state.set_state(ControlStates.waiting_mail)
    return await m.answer(mailing_prompt())


@router.message(Command("cancel"), ControlStates.waiting_mail, flags={"delay": 1})
async def mailing_cancel(m: Message, state: FSMContext) -> None:
    await state.clear()
    return await m.answer(mailing_cancelled())


@router.message(ControlStates.waiting_mail, flags={"delay": 2})
async def mailing_wait(
    m: Message, bot: Bot, session: sessionmaker, state: FSMContext
) -> None:
    text = m.html_text or m.text
    if not text:
        return await m.answer("Send a text message or /cancel")

    sql_user = SQLUser(session)
    users = await sql_user.all()
    recipients = [user for user in users if not user.is_blocked]
    skipped = len(users) - len(recipients)

    await m.answer(mailing_started(len(recipients)))
    await state.clear()

    start_time = dt.now()
    sent = 0
    failed = 0
    blocked = 0

    for user in recipients:
        try:
            await bot.send_message(chat_id=user.user_id, text=text)
            sent += 1
        except (TelegramBadRequest, TelegramForbiddenError):
            blocked += 1
            await sql_user.update(user_id=user.user_id, is_blocked=True)
        except ValidationError:
            failed += 1
        except Exception:
            failed += 1

    total_sec = (dt.now() - start_time).total_seconds()
    return await m.answer(
        mailing_report(
            sent=sent,
            failed=failed,
            blocked=blocked,
            skipped=skipped,
            seconds=total_sec,
        )
    )


# Псевдоним
router_mailing = router
