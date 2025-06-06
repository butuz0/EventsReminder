from aiogram.fsm.state import State, StatesGroup


class VerificationStates(StatesGroup):
    unverified = State()
    verified = State()
