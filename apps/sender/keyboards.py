from typing import Optional
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class SenderCallback(CallbackData, prefix="sdr"):
    level: int
    tid: int
    confirm: bool = True


class SenderHistoryCallback(CallbackData, prefix="shs"):
    level: int
    page: int


def make_sender_cd(level, tid=0):
    return SenderCallback(level=level, tid=tid).pack()


def make_sender_history_cd(level, page=1):
    return SenderHistoryCallback(level=level, page=page).pack()


def sender_options():
    CURRENT_LEVEL = 1
    builder = InlineKeyboardBuilder()
    builder.row(
        *[
            InlineKeyboardButton(
                text="Создать 🚀", callback_data=make_sender_cd(CURRENT_LEVEL + 1)
            ),
            InlineKeyboardButton(
                text="История 📝", callback_data=make_sender_history_cd(CURRENT_LEVEL)
            ),
        ]
    )
    builder.row(
        InlineKeyboardButton(
            text="⬅️ Назад", callback_data=make_sender_cd(CURRENT_LEVEL - 1)
        )
    )
    return builder.as_markup()


def sender_skip_or_cancel(
    step: Optional[str] = None,
    has_skip: bool = False,
    has_previous: bool = False,
    has_next: bool = True,
):
    builder = InlineKeyboardBuilder()
    if has_skip:
        board = []
        if has_next:
            board.append(
                InlineKeyboardButton(
                    text="Пропустить ➡️", callback_data=f"sender:next:{step}"
                ),
            )
        if has_previous:
            board.insert(
                0,
                InlineKeyboardButton(
                    text="⬅️ Назад", callback_data=f"sender:prev:{step}"
                ),
            )
        builder.row(*board)
    builder.row(
        InlineKeyboardButton(text="Отмена ❌", callback_data=f"sender:cancel:{step}")
    )
    return builder.as_markup()


def confirm_keyboard(step: Optional[str] = None, **kwargs):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Да ✅", callback_data=f"sender:confirm:{step}")
    )
    builder.row(
        InlineKeyboardButton(
            text="Показать шаблон 📝", callback_data=f"sender:show_t:{step}"
        )
    )
    builder.row(
        InlineKeyboardButton(text="⬅️ Назад", callback_data=f"sender:prev:{step}"),
        InlineKeyboardButton(text="Отмена ❌", callback_data=f"sender:cancel:{step}"),
    )
    return builder.as_markup()


def sender_hs_paginate(has_next: bool = False, has_prev: bool = False, page: int = 1):
    builder = InlineKeyboardBuilder()
    board = []
    if has_prev:
        board.append(InlineKeyboardButton(text="⬅️", callback_data=make_sender_history_cd(1, page-1)))
    if has_next:
        board.append(InlineKeyboardButton(text="➡️", callback_data=make_sender_history_cd(1, page+1)))
    builder.row(*board)
    builder.row(
        InlineKeyboardButton(text="⬅️ Назад", callback_data=make_sender_cd(1))
    )
    return builder.as_markup()


def myself_delete():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Скрыть ❌", callback_data="delete_myself"))
    return builder.as_markup()
