from aiogram.fsm.state import State, StatesGroup


class SenderState(StatesGroup):
  image = State()
  text = State()
  confirm = State()