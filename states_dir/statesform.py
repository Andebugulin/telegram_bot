from aiogram.fsm.state import StatesGroup, State


class StepsForm(StatesGroup):
    MENU = State()

    TEMPLATE = State()
    TEMPLATE_ADD = State()
    TEMPLATE_DELETE = State()
    WORKING = State()
    WORKING_START = State()
    WORKING_ADD = State()
    WORKING_DELETE = State()