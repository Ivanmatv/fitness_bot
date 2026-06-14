from aiogram.fsm.state import State, StatesGroup


class WorkoutStates(StatesGroup):
    waiting_for_sport = State()
    waiting_for_intensity = State()
