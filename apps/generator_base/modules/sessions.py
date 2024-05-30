import asyncio
import aiohttp
import aiohttp.http_exceptions

from loguru import logger



class BaseSession:
    def __init__(self, max_retries=15, retry_delay=1):
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    async def _make_request(self, url: str, method: str = "GET", response_type: str = "text", **kwargs):
        for attempt in range(self.max_retries):
            try:
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=100)) as session:
                    async with session.request(method, url, **kwargs) as response:
                        response.raise_for_status()
                        if response_type == "json":
                            return await response.json()
                        elif response_type == "text":
                            return await response.text()
                        elif response_type == "binary":
                            return await response.read()
                        else:
                            raise ValueError("Некорректный тип ожидаемого ответа...")
            except (
                aiohttp.ClientError, 
                aiohttp.http_exceptions.HttpProcessingError, 
                asyncio.TimeoutError
            ) as e:
                logger.error(f"Попытка {attempt + 1} окончена с ошибкой: {e}")
                await asyncio.sleep(self.retry_delay)
        return None
    
    async def fetch_image(self, url: str):
        return await self._make_request(url, response_type="binary")
    
