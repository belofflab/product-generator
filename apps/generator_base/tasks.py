from apscheduler.triggers.cron import CronTrigger


from loader import bot
from aiogram.types import InputMediaDocument, FSInputFile
from apps.generator_base.modules.cards.saver import Saver
from apps.generator_base.modules.cards import Generator
from apps.generator_base.modules.cards.exceptions import CardGenFailed

from config.settings import MEDIA_DIR

every_day_trigger = CronTrigger(hour=18, minute=40)
every_week_trigger = CronTrigger(day_of_week="mon")
every_month_trigger = CronTrigger(day="1")



async def get_report_task(chat_id: int, message_id: str):
        new_message = await bot.send_message(chat_id=chat_id, text="Формируем ваш отчёт...")
        try:
            Saver(chat_id).make_report()
            await bot.delete_message(chat_id, message_id)
            await new_message.delete()
            await bot.send_document(chat_id=chat_id, document=FSInputFile(MEDIA_DIR / f"user_cards/{chat_id}/report.xlsx"), caption="Вот ваш отчёт!")
        except Exception as error:
            await new_message.edit_caption(caption=f"Ошибка: {error}. Пожалуйста, попробуйте позже!")


async def generate_card_task(chat_id: int, file_id: str, message_id: str):
        new_message = await bot.send_photo(chat_id=chat_id, photo=file_id, caption="<b>Новая задача на генерацию карточки!</b>\n\nВремя ожидания: 5-6 минут.\n\n<i>Описание под данным фото будет изменено после генерации карточки.</i>")
        try:
            card = await Generator(chat_id).make_card(file_id)
            await bot.delete_message(chat_id, message_id)
            await new_message.edit_caption(caption=f"""
<b>Добавлена новая карточка!</b>
                                    
<b>Наименование: </b> <code>{card.name}</code>
<b>Описание: </b> <code>{card.description}</code>

<i>Разработано: @belofflab</i>
""")
        except CardGenFailed as error:
            await new_message.edit_caption(caption=f"Ошибка: {error}. Пожалуйста, попробуйте позже!")