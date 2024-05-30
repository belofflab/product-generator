from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from apps.sender.keyboards import make_sender_cd

def admin():
    CURRENT_LEVEL = 0
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Рассылка 🚀", callback_data=make_sender_cd(CURRENT_LEVEL + 1)
        ),
    )
    return builder.as_markup()
