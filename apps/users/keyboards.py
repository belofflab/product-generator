from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Extra modules

def start():
    CURRENT_LEVEL = 0
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Под ключ 📦", url="https://t.me/t.me/AlexArmada20"),
        InlineKeyboardButton(text="Помощь ⚙️", url="https://t.me/belofflab"),   
    )
    builder.row(
        InlineKeyboardButton(text="Сотрудничество 🧑‍💼", url="https://t.me/AlexArmada20"),
    )
    return builder.as_markup()
