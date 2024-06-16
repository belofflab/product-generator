from aiogram import Router
from aiogram.types import ErrorEvent

from loguru import logger

router = Router()


@router.error()
async def any_error(event: ErrorEvent, **kwargs):
  logger.error(event) 