from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from apps.users.middlewares import UserExistsMiddleware
from apscheduler.triggers.date import DateTrigger
from apps.generator_base.tasks import generate_card_task, get_report_task
from loader import scheduler
router = Router()
router.message.middleware(UserExistsMiddleware())


@router.message(Command("report"))
async def report(message: Message):
    user_id = message.from_user.id
    message_id = message.message_id
    scheduler.add_job(get_report_task, trigger=DateTrigger(), args=(user_id, message_id))

@router.message(F.content_type == 'photo')
async def generate_card(message: Message):
    user_id = message.from_user.id
    photo = message.photo[-1]
    file_id = photo.file_id
    message_id = message.message_id
    scheduler.add_job(generate_card_task, trigger=DateTrigger(), args=(user_id, file_id, message_id))

    