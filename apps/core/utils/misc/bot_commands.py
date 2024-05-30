# - *- coding: utf- 8 - *-
from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault

from apps.users.services import UserService

# Команды для юзеров
user_commands = [
    BotCommand(command='start', description='♻️ Перезапустить бота'),
]

# Команды для админов
admin_commands = [
    *user_commands,
    BotCommand(command='admin', description='Админ-панель'),
]


# Установка команд
async def set_commands(bot: Bot):
    await bot.set_my_commands(user_commands, scope=BotCommandScopeDefault())

    for admin in UserService.get_admins():
        try:
            await bot.set_my_commands(admin_commands, scope=BotCommandScopeChat(chat_id=admin))
        except Exception as ex:
            print(ex)
