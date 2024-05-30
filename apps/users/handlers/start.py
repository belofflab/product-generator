from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from apps.users import keyboards
from apps.users.middlewares import UserExistsMiddleware
from config.settings import MEDIA_DIR
from apps.core.utils.misc.extras import answer_or_edit_photo


router = Router()
router.message.middleware(UserExistsMiddleware())


@router.message(Command("start"))
async def start(callback: Message, state: FSMContext = None, **kwargs):
    await answer_or_edit_photo(
        callback,
        photo=FSInputFile(MEDIA_DIR / "banner.webp"),
        caption=f"Добро пожаловать, {callback.from_user.full_name}!\n\nДля генерации карточки просто пришлите фотографию!",
        reply_markup=keyboards.start(),
    )