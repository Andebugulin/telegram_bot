from aiogram.fsm.state import StatesGroup, State


class StepsForm(StatesGroup):
    MENU = State()
    START = State()
    ADD = State()
    DELETE = State()
    TEMPLATE = State()
    TEMPLATE_ADD = State()
    TEMPLATE_DELETE = State()