from aiogram.fsm.state import State, StatesGroup


class Output(StatesGroup):
    stack = State()