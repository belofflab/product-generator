from typing import Union
from fastapi import HTTPException
from aiogram.types import Message, CallbackQuery
from config.database import DatabaseManager
from sqlalchemy import select, func
from loader import bot 
from config.settings import MEDIA_DIR

class StepWrap:
    default_value = "0"

    def __init__(self, steps: str = None) -> None:
        self.steps = steps if steps is not None else self.default_value

    def has_steps(self):
        return len(self.steps) > len(self.default_value)

    def get_last_step(self, is_target: bool = False):
        if not self.has_steps():
            return self.default_value
        steps = self.steps.split(".")
        if is_target and len(steps) > 1:
            return int(steps[-2])
        return int(steps[-1])

    def add_next_step(self, step: int):
        self.steps = self.steps + f".{step}" if self.has_steps() else str(step)
        return self.steps

    def remove_last_step(self, is_target: bool = False):
        steps = self.steps.split(".")
        if len(steps) == 1:
            self.steps = self.default_value
            return self.steps
        if is_target and len(steps) > 1:
            steps.pop(-2)
        else:
            steps.pop()
        self.steps = ".".join(steps)
        return self.steps


class Paginator:
    MAX_PER_PAGE_ITEMS = 1000
    def __init__(self, query, page, per_page) -> None:
        self.query = query
        self.page = page
        self.per_page = int(per_page)
        if self.per_page > self.MAX_PER_PAGE_ITEMS:
            raise HTTPException(status_code=403, detail="Go away ")
        self.limit = per_page * page
        self.offset = (page - 1) * per_page
        self.number_of_pages = 0
        self.next_page = ""
        self.previous_page = ""

    def _get_next_page(self) -> bool:
        if self.page >= self.number_of_pages:
            return False
        return True

    def _get_previous_page(self) -> bool:
        if self.page == 1 or self.page > self.number_of_pages + 1:
            return False
        return True

    def _get_number_of_pages(self, count: int) -> int:
        rest = count % self.per_page
        quotient = count // self.per_page
        return quotient if not rest else quotient + 1

    def _get_total_count(self) -> int:
        count = DatabaseManager.session.scalar(
            select(func.count()).select_from(self.query.subquery())
        )
        self.number_of_pages = self._get_number_of_pages(count)
        return count

    def get_response(self, serializer = None, **kwargs) -> dict:
        return {
            "count": self._get_total_count(),
            "pages": self.number_of_pages,
            "next_page": self._get_next_page(),
            "previous_page": self._get_previous_page(),
            "items": [
                serializer(item.id, **kwargs) if serializer is not None else item
                for item in DatabaseManager.session.scalars(
                    self.query.limit(self.limit).offset(self.offset)
                )
            ],
        }


async def download_image(message: Message):
    destination = f"{message.photo[-1].file_id}.jpg"
    await bot.download(message.photo[-1], destination=MEDIA_DIR / destination)
    return destination

async def answer_or_edit_message(message: Union[Message, CallbackQuery], **kwargs):
    if isinstance(message, Message):
        await message.answer(**kwargs)
    elif isinstance(message, CallbackQuery):
        await message.message.edit_text(**kwargs)


async def answer_or_edit_photo(message: Union[Message, CallbackQuery], **kwargs):
    if isinstance(message, Message):
        await message.answer_photo(**kwargs)
    elif isinstance(message, CallbackQuery):
        await message.message.edit_caption(**kwargs)