import typing as t
from aiogram import BaseMiddleware
from aiogram.types import Message
from apps.users.services import UserService


class UserExistsMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.current_user = {}

    async def __call__(
        self,
        handler: t.Callable[[Message, t.Dict[str, t.Any]], t.Awaitable[t.Any]],
        event: Message,
        data: t.Dict[str, t.Any],
    ) -> t.Any:
        self.current_user = UserService.create_or_update_user(
            id=event.from_user.id,
            username=event.from_user.username,
            full_name=event.from_user.full_name,
        )
        data["current_user"] = self.current_user

        return await handler(event, data)
