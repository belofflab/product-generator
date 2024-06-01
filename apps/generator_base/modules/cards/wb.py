import json 
import os 
from typing import Optional, List
from apps.generator_base.models import UserCard
from apps.generator_base.modules.sessions import BaseSession
from apps.generator_base.modules.cards.exceptions import ProductsGetFailed
from config.settings import MEDIA_DIR

from loguru import logger

class WB:
    def __init__(self, user_card: Optional[UserCard] = None) -> None:
        self.http_client = BaseSession(max_retries=5)
        self.user_card = user_card
    
    async def get_similar_queries(self, query: str):
        headers = {
            'accept': '*/*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'origin': 'https://www.wildberries.ru',
            'priority': 'u=1, i',
            'referer': 'https://www.wildberries.ru/catalog/0/search.aspx?search=%D1%81%D1%83%D0%BC%D0%BA%D0%B0%20%D0%B6%D0%B5%D0%BD%D1%81%D0%BA%D0%B0%D1%8F%20%D1%88%D0%BE%D0%BF%D0%BF%D0%B5%D1%80',
            'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'x-queryid': 'qid469165812171597696620240530125324',
        }

        params = {
            'query': query,
            'lang': 'ru',
            'appType': '1',
            'curr': 'rub',
            'dest': '-1257786',
            'spp': '30',
            'locale': 'ru',
            'ab_testing': 'false',
        }
        return await self.http_client._make_request(method="GET", url='https://similar-queries.wildberries.ru/api/v2/search/query', response_type="json", params=params, headers=headers)

    async def get_product_path(self, nm_id: int, subject: str, brand: str) -> dict:
        headers = {
            'accept': '*/*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'priority': 'u=1, i',
            'referer': f'https://www.wildberries.ru/catalog/{nm_id}/detail.aspx',
            'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'x-spa-version': '10.0.11.4',
        }
        params = {
            'subject': subject,
            'kind': '0',
            'brand': brand,
        }
        return await self.http_client._make_request(
            method="GET",
            url=f'https://www.wildberries.ru/webapi/product/{nm_id}/data',
            response_type="json",
            params=params,
            headers=headers
        )

    async def get_product(self, nm_id: int) -> dict:
        volume = self.__get_product_volume(nm_id)

        headers = {
            'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'Referer': f'https://www.wildberries.ru/catalog/{nm_id}/detail.aspx?targetUrl=EX',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'sec-ch-ua-platform': '"macOS"',
        }

        return await self.http_client._make_request(url=f'{volume}/info/ru/card.json', response_type="json", headers=headers)


    async def get_products(self, query: str) -> Optional[List[dict]]:
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Origin': 'https://www.wildberries.ru',
            'Referer': 'https://www.wildberries.ru/catalog/0/search.aspx?page=1&sort=popular&search=%D0%B4%D1%83%D1%85%D0%B8+%D0%B6%D0%B5%D0%BD%D1%81%D0%BA%D0%B8%D0%B5',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'x-queryid': 'qid469165812171597696620240525054354',
        }
        params = {
            'ab_testing': 'false',
            'appType': '1',
            'curr': 'rub',
            'dest': '-1257786',
            'page': '1',
            'query': query,
            'resultset': 'catalog',
            'sort': 'popular',
            'spp': '30',
            'suppressSpellcheck': 'false',
        }

        products =  await self.http_client._make_request(
            url='https://search.wb.ru/exactmatch/ru/common/v5/search', 
            method="GET", response_type="text", params=params, headers=headers
        )
        try:
            product_obj = json.loads(products)
            products_list = product_obj.get("data", {}).get("products", [])
            if len(products_list) >= 1:
                return products_list
        except Exception as ex:
            logger.error(f"Error: {ex}")
            pass 
        raise ProductsGetFailed("не удалось проанализировать конкурентов на WB.")
    
    async def match_product(self, product_name: str) -> dict:
        products = await self.get_products(product_name)

        first_product = products[0]
        nm_id = first_product['id']
        extra_data = await self.get_product(nm_id)
        def black_check(option_name: Optional[str]):
            if option_name is None: return False
            blacklist_options = ['вид', 'тип', 'комплектация']
            for bl_option in blacklist_options:
                if bl_option in option_name.lower():
                    return False
            return True
        clean_obj = {
            "wb_name": extra_data.get("imt_name"),
            "brand": extra_data.get("selling", {}).get("brand_name"),
            "category_name": extra_data.get("subj_name"),
            "wb_description": extra_data.get("description"),
            "options": [option for option in extra_data.get("options", []) if black_check(option.get('name'))]
        }
        sizes_table = extra_data.get("sizes_table")
        if sizes_table is not None:
            extra_data["sizes_table"] = "; ".join([value["tech_size"] for value in extra_data.get("sizes_table", {}).get("values", [])])
        path = MEDIA_DIR / f"user_cards/{self.user_card.user_id}/{self.user_card.id}"
        try:
            os.makedirs(path, exist_ok=True)
            with open(path / "card.json", "w", encoding="utf-8") as f:
                json.dump(clean_obj, f, ensure_ascii=False)
        except Exception as ex:
            logger.error(f"Error: {ex}")
            pass

        return clean_obj
    
    @staticmethod
    def __get_product_volume(nm_id: int) -> str:
        _short_id = nm_id // 100000

        if 0 <= _short_id <= 143:
            basket = '01.wb'
        elif 144 <= _short_id <= 287:
            basket = '02.wb'
        elif 288 <= _short_id <= 431:
            basket = '03.wb'
        elif 432 <= _short_id <= 719:
            basket = '04.wb'
        elif 720 <= _short_id <= 1007:
            basket = '05.wb'
        elif 1008 <= _short_id <= 1061:
            basket = '06.wb'
        elif 1062 <= _short_id <= 1115:
            basket = '07.wb'
        elif 1116 <= _short_id <= 1169:
            basket = '08.wb'
        elif 1170 <= _short_id <= 1313:
            basket = '09.wb'
        elif 1314 <= _short_id <= 1601:
            basket = '10.wb'
        elif 1602 <= _short_id <= 1655:
            basket = '11.wb'
        elif 1656 <= _short_id <= 1919:
            basket = '12.wb'
        elif 1920 <= _short_id <= 2045:
            basket = '13.wb'
        elif 2046 <= _short_id <= 2189:
            basket = '14.wb'
        elif 2190 <= _short_id <= 2405:
            basket = '15.wbbasket'
        elif 2406 <= _short_id <= 2621:
            basket = '16.wbbasket'
        else:
            basket = '17.wbbasket'

        return f"https://basket-{basket}.ru/vol{_short_id}/part{nm_id // 1000}/{nm_id}"
    
wb = WB


if __name__ == "__main__":
    result = wb().get_products("Мужские духи Dior")
    if result is None:
        print("Не нашли ничего по заданному запросу")
    else:
        print(result)
        print(f"Найдено товаров: {len(result)}")