from aiogram import Router
from aiogram.types import ErrorEvent
from apps.admin.middlewares import IsAdminMiddleware
from loguru import logger
router = Router()
router.message.middleware(IsAdminMiddleware())


# @router.error()
# async def any_error(event: ErrorEvent, **kwargs):
#   logger.error(event) 