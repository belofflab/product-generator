from typing import Optional
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from apps.core.utils.misc.extras import StepWrap


class CategoryCallback(CallbackData, prefix="cat"):
    level: int
    cstep: str = "0"
    page: int


def make_category_cd(level, page=1, cstep: Optional[str] = "0"):
    return CategoryCallback(level=level, page=page, cstep=cstep).pack()


def list_categories(
    items: list,
    page: int,
    sw: StepWrap,
    has_previous_page: bool,
    has_next_page: bool,
    is_admin: bool = False,
):
    CURRENT_LEVEL = 1
    builder = InlineKeyboardBuilder()
    if is_admin:
        builder.row(
            InlineKeyboardButton(
                text="Добавить категорию ✅", callback_data="move_category:add:0"
            )
        )
    for item in items:
        builder.row(
            InlineKeyboardButton(
                text=item["name"],
                callback_data=(
                    make_category_cd(
                        level=CURRENT_LEVEL,
                        page=page,
                        cstep=StepWrap(sw.steps).add_next_step(
                            step=item["category_id"]
                        ),
                    )
                    if item["has_children"]
                    else "-"
                ),
            )
        )
    board = []
    if has_previous_page:
        board.append(
            InlineKeyboardButton(
                text="Назад ⬅️",
                callback_data=make_category_cd(
                    level=CURRENT_LEVEL, cstep=sw.steps, page=page - 1
                ),
            )
        )
    if has_next_page:
        board.append(
            InlineKeyboardButton(
                text="Далее ➡️",
                callback_data=make_category_cd(
                    level=CURRENT_LEVEL, cstep=sw.steps, page=page + 1
                ),
            )
        )
    builder.row(*board)
    builder.row(
        InlineKeyboardButton(
            text="⬅️ Вернуться",
            callback_data=make_category_cd(
                level=(CURRENT_LEVEL if sw.has_steps() else CURRENT_LEVEL - 1),
                page=page,
                cstep=(sw.remove_last_step() if sw.has_steps() else sw.steps),
            ),
        )
    )
    return builder.as_markup()