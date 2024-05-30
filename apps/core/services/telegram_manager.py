import asyncio
from typing import List
from config.settings import TGServiceConfig
from loader import bot
from apps.core.date_time import DateTime
from apps.users.models import User


class TGService:
    config = TGServiceConfig.get_config()

    @classmethod
    async def __send_message(cls, chat_id: int, text: str, **kwargs):
        try:
            await bot.send_message(chat_id=chat_id, text=text, **kwargs)
        except Exception as ex:
            print(ex)

    @classmethod
    async def to_user(cls, chat_id: int, text: str):
        await cls.__send_message(chat_id, text)

    @classmethod
    async def to_admins(cls, text: str, **kwargs):
        """
        Sending Message to admins
        """
        admins = User.filter(User.is_admin == True).all()
        for admin in admins:
            await asyncio.sleep(0.03)
            await cls.__send_message(chat_id=admin.id, text=text, **kwargs)

    @classmethod
    async def to_subscribers(cls, text: str, **kwargs):
        """
        Sending Message to subscribers
        """
        subscribers = User.filter(User.is_subscribed == True).all()
        for subscriber in subscribers:
            await asyncio.sleep(0.03)
            await cls.__send_message(chat_id=subscriber.id, text=text, **kwargs)

    @classmethod
    async def _to_notification_chat(cls, text: str, **kwargs):
        """
        Sending Message to notification chat
        """
        await cls.__send_message(chat_id=cls.config.chat_id, text=text, **kwargs)