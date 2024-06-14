import os 

from loguru import logger

from apps.generator_base.models import UserCard

from apps.generator_base.modules.sessions import BaseSession
from apps.generator_base.modules.cards.ai import AI
from apps.generator_base.modules.cards.wb import WB
from apps.generator_base.modules.cards.saver import Saver
from apps.generator_base.modules.cards.exceptions import CardGenFailed, GPTAccessFailed, ProductsGetFailed

from config.settings import MEDIA_DIR

from loader import bot, cfg

class Generator:
    def __init__(self, user_id: int) -> None:
        self.http_client = BaseSession(max_retries=5)

        self.user_id = user_id
        self.new_card = None

    async def make_card(self, file_id: str):
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path
        image_content = await self.http_client.fetch_image(f"https://api.telegram.org/file/bot{cfg.bot_token}/{file_path}")
        try:
            gpt_data = await AI().generate_card(image_content)
            # gpt_data = {"name": "Кроссовки Adidas", "description": "Top", "size": "10x10x10"}
            self.new_card = UserCard.create(user_id=self.user_id, **gpt_data)
            path = MEDIA_DIR / f"user_cards/{self.new_card.user_id}/{self.new_card.id}"
            try:
                os.makedirs(path, exist_ok=True)
                with open(path / "input_image.png", "wb") as f:
                    f.write(image_content)
            except Exception as ex:
                print(f"Error: {ex}")
                pass
        except GPTAccessFailed as e:
            logger.error(f"GPT access failed: {e}")
            raise CardGenFailed("интеллект перегружен")
        try:
            await WB(user_card=self.new_card).match_product(product_name=gpt_data.get('name'))
        except ProductsGetFailed as ex:
            raise CardGenFailed(ex, self.new_card.id)

        Saver(self.user_id).make_report(self.new_card.id)

        return self.new_card
    


generator = Generator