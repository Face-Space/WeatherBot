from aiogram.fsm.state import StatesGroup, State


class UserSelect(StatesGroup):
    city = State()
    note = State()

    my_user = None
    continuation = None
    my_city = None
