import re
import asyncio
import json
import aiohttp

import aiohttp.client_exceptions
import aiohttp.web_exceptions
import aiohttp.http_exceptions

from g4f.Provider import OpenaiAccount, Bing
from g4f.client import Client
from g4f.cookies import set_cookies
from g4f.errors import RateLimitError, ResponseStatusError
from loguru import logger

from apps.generator_base.modules.cards.wb import WB
from apps.generator_base.modules.cards.exceptions import GPTAccessFailed, GPTWrapResponseFailed
from apps.generator_base.modules.sessions import BaseSession

BING_API_KEY = "1xtv19K7vNQy2NvZqE_wo3tjbCeQOcCrroOo1dEs_HKSWr_XrSoLODQNf9YnnOA7iAR2TVwsnyahkq2rim3OgdnxupkjyssJmdq0uF6RxZy48erjmNZiIVB3-zlKBnroDDL0aasR_CJT_KFJdNblwvYjthRyrtP9SJIWZn10PPWVvL_1-9k5azmqDYdBQFnixIVFHFSBudonhtaSFLXaS5A"

class AI:
    def __init__(self) -> None:
        self.http_session = BaseSession()
        self.client = Client(provider=Bing)

        set_cookies(".bing.com", {
            "_U": BING_API_KEY
        })
    
    async def ask_gpt(
            self, 
            prompt: str, 
            image_content: bytes = None, 
            model: str = "gpt-4-turbo", 
            max_tokens: int = 1500,
            hasWrap: bool = False
        ) -> dict:
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                },
            ]
        }
        if image_content is not None:
            payload["image"] = image_content
        max_attempts = 5
        attempt = 0
        timeout_delay = 3
        while True:
            attempt = attempt + 1
            try:
                logger.info(f"Отправляем запрос в интеллект. Попытка: {attempt}")
                response = self.client.chat.completions.create(**payload)
                if hasWrap:
                    return self.__wrap_gpt_response(response.choices[0].message.content)
                else:
                    return response.choices[0].message.content
            except aiohttp.client_exceptions.ServerDisconnectedError as ex:
                logger.error(f"Ошибка подключения; Код: {ex}.")
            except RateLimitError as ex:
                logger.error(f"RateLimitError: {ex}")
                await asyncio.sleep(90)
            except (ResponseStatusError, GPTWrapResponseFailed) as ex:
                logger.error(f"Error: {ex}")
                await asyncio.sleep(10)
            except Exception as error:
                logger.error(f"Неизвестная ошибка: {error}")
            await asyncio.sleep(timeout_delay)
            if attempt >= max_attempts:
                raise GPTAccessFailed("Не удалось получить доступ к интеллекту")

    def __extract_dimensions(self, dimension_string: str) -> str:
        pattern = re.compile(r'(\d*\.?\d+)\s*x\s*(\d*\.?\d+)\s*x\s*(\d*\.?\d+)')
        match = pattern.match(dimension_string)
        if match:
            return 'x'.join(match.groups())
        else:
            return "Не смогли определить размер на фотографии"

    def __wrap_gpt_response(self, response_content: str) -> dict:
        try:
            json_match = re.search(r'{.*}', response_content, re.DOTALL)
            if json_match:
                json_object = json_match.group(0)
                dictionary = json.loads(json_object)
                is_success = bool(int(dictionary.get("is_success", 0)))
                if is_success:
                    dictionary.pop('is_success', None)
                    return dictionary
        except Exception as error_msg:
            logger.error(f"При обработке карточки возникла ошиюка: {error_msg}")
        
        raise GPTWrapResponseFailed("Произошла ошибка обработки карточки.")
    
    async def generate_card(self, image_content: bytes) -> dict:
        # prompt: str = """Identify the item in the photo (this thing can be put on a person), write best selling descriptions (on russian language) of the item in the photo for marketplace, write the average size of the item in the photo in a given format without too much explanation. Size format: height x length x width (without letters only integer). Give me JSON object with values. Don't text me any other information besides the JSON object For Example {"name":"full item name (must be < 60 chars, must describe the item in the picture in detail for the seo and contain perhaps a make, model, color or material).", "description": "item description with selling SEO (use keywords similar to this one) (min 1500 characters, max 2000 characters)", "size": "height x width x length in centimeter" ,"is_success": "1 if success else 0"}"""
        card = {}
        prompt_one: str = """Identify the item in the photo (this thing can be put on a person). write the average size of the item in the photo in a given format without too much explanation. Give me JSON object with values. Don't text me any other information besides the JSON object. For Example {"name":"full item name (must be < 60 chars, must describe the item in the picture in detail for the seo and contain perhaps a make, model, color or material). on russian language", "size": "height x width x length in centimeter" ,"is_success": "1 if success else 0"}"""
        
        card_data = await self.ask_gpt(prompt_one, image_content, model="gpt-4-turbo", max_tokens=500, hasWrap=True)
        name = card_data.get("name")
        size = card_data.get("size")
        if name is None or size is None:
            raise GPTAccessFailed("проблема с получением объекта.")
        else:
            card["name"] = name
            card["size"] = self.__extract_dimensions(size)

        similar_queries_data = await WB().get_similar_queries(name)
        similar_queries = similar_queries_data.get("query", [])

        # prompt_two: str = f"""You are a copywriter in our company. I sell {name}. Based on the keywords, write an SEO description which should be at least 2000 characters without own comments. keywords: {','.join(query for query in similar_queries)}. For Example {{"description":"on russian language. minimum 3000 characters!","is_success": "1 if success else 0"}}"""
        prompt_two: str = f"""You are a copywriter in our company. I sell {name}. Based on the keywords, write an SEO description which should be at least 2000 characters. don't write notes from yourself, just a description. Don't emphasise words. Keywords: {','.join(query for query in similar_queries)}."""
        description = await self.ask_gpt(prompt_two, model="gpt-4-turbo", max_tokens=2300)
    
        card["description"] = description

        return card
    
