from enum import IntEnum

from aiogram.filters.callback_data import CallbackData


class BasicAction(IntEnum):
    """
    Действия с базовым функционалам
    """

    SELECT_AUDIO = 0
    SELECT_VIDEO = 1


class BasicCallback(CallbackData, prefix="state"):
    """
    Обработка действий базового функционала
    """

    action: BasicAction
