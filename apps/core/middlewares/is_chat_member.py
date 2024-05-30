import typing as t
from aiogram import BaseMiddleware

from aiogram.types import Message
from loader import bot


class IsChatMember(BaseMiddleware):
    async def __please_subscribe(self, event: Message):
        await bot.send_message(chat_id=event.from_user.id, text="Пожалуйста, подпишитесь на наш канал")

    async def __call__(
        self,
        handler: t.Callable[[Message, t.Dict[str, t.Any]], t.Awaitable[t.Any]],
        event: Message,
        data: t.Dict[str, t.Any],
    ) -> t.Any:
        member = await bot.get_chat_member(chat_id=-4106035615, user_id=event.from_user.id)
        if member.status.value != "left":
          return await handler(event, data)
        else:
            return await self.__please_subscribe(event)
