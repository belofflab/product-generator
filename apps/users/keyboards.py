from typing import Optional
from decimal import Decimal
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class RefillCallback(CallbackData, prefix="rfl"):
    level: int
    tid: Optional[int] = None
    confirm: bool = False


def make_refill_cd(level, tid: Optional[int] = None, confirm: bool = False):
    return RefillCallback(level, tid, confirm).pack()


def start():
    CURRENT_LEVEL = 0
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Пополнить баланс", callback_data=make_refill_cd(CURRENT_LEVEL + 1)
        ),
    )
    builder.row(
        InlineKeyboardButton(text="Под ключ 📦", url="https://t.me/t.me/AlexArmada20"),
        InlineKeyboardButton(text="Помощь ⚙️", url="https://t.me/belofflab"),
    )
    builder.row(
        InlineKeyboardButton(
            text="Сотрудничество 🧑‍💼", url="https://t.me/AlexArmada20"
        ),
    )
    return builder.as_markup()


def ask_amount():
    CURRENT_LEVEL = 1
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Отмена", callback_data=make_refill_cd(CURRENT_LEVEL - 1)
        ),
    )
    return builder.as_markup()

def confirm_refill():
    CURRENT_LEVEL = 1
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Да", callback_data=make_refill_cd(CURRENT_LEVEL + 1, confirm=True)
        ),
        InlineKeyboardButton(
            text="Нет", callback_data=make_refill_cd(CURRENT_LEVEL - 1, confirm=False)
        ),
    )
    return builder.as_markup()


def proceed_refill(tid: int):
    CURRENT_LEVEL = 2
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Я оплатил",
            callback_data=make_refill_cd(CURRENT_LEVEL, tid=tid, confirm=True),
        )
    )
    return builder.as_markup()
