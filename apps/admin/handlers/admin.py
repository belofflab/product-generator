from aiogram import Router
from aiogram.filters import Command
from aiogram import types
from apps.admin import keyboards
from apps.admin.middlewares import IsAdminMiddleware

from apps.core.utils.misc.extras import answer_or_edit_message

router = Router()
router.message.middleware(IsAdminMiddleware())


@router.message(Command("admin"))
async def admin(callback: types.Message, **kwargs):
    await answer_or_edit_message(
        message=callback,
        text=f"Добро пожаловать, {callback.from_user.full_name}",
        reply_markup=keyboards.admin(),
    )