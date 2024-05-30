from typing import Optional
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class CardCallback(CallbackData, prefix="card"):
    level: int
    card_id: Optional[int]
    page: int


def make_card_cd(level, card_id: Optional[int] = None, page: int = 1):
    return CardCallback(level=level, card_id=card_id, page=page).pack()


def list_cards(items: list, has_prev: bool, has_next: bool, page: int = 1, **kwargs):
    CURRENT_LEVEL = 1
    builder = InlineKeyboardBuilder()
    for item in items:
        builder.row(InlineKeyboardButton(
            text=item["card"]["name"],
            callback_data=make_card_cd(level=CURRENT_LEVEL + 1, card_id=item["card"]["card_id"], page=1)
        ))
    board = []
    if has_prev:
        board.append(
            InlineKeyboardButton(
                text="Назад ⬅️",
                callback_data=make_card_cd(
                    level=CURRENT_LEVEL, page=page - 1
                ),
            )
        )
    if has_next:
        board.append(
            InlineKeyboardButton(
                text="Далее ➡️",
                callback_data=make_card_cd(
                    level=CURRENT_LEVEL, page=page + 1
                ),
            )
        )
    builder.row(*board)
    builder.row(
        InlineKeyboardButton(
            text="⬅️ Вернуться",
            callback_data=make_card_cd(level=CURRENT_LEVEL - 1, page=page),
        )
    )
    return builder.as_markup()

async def show_card(card_id: int, page: int):
    CURRENT_LEVEL = 2
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="⬅️ Вернуться",
            callback_data=make_card_cd(CURRENT_LEVEL - 1, card_id=card_id, page=page)
        )
    )
    return builder.as_markup()