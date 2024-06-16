from aiogram.fsm.state import State, StatesGroup


class RefillState(StatesGroup):
  amount = State()
  confirm = State()