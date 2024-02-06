from aiogram.fsm.state import State, StatesGroup


class ControlStates(StatesGroup):
    """
    Состояния центра управления
    """

    waiting_mail = State()
