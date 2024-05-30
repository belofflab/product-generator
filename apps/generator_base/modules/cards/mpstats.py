


from apps.generator_base.modules.sessions import BaseSession


class MPStats:
    BASE_URL = 'https://mpstanalitika.pro/api/seo/description-generator'
    def __init__(self) -> None:
        self.http_session = BaseSession()

    async def make_report(self, product_name: str, key_words: list, length: str = "char_1000", tone_of_voice: int = 1, advantages: list = [""], minus_words: list = [""]):
        url = f'{self.BASE_URL}/make-report'
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'cookie': 'connect.sid=s%3AIjo0ckBExt4pvFwy7Dg0bYagizfHRpTg.uI9Jo32aDht%2F5WUj%2BNQayzvqctEpk1DwmmQVAZJJPaI; _mpsuid=531de0502eb48c4c0511f724d3d059f1',
            'origin': 'https://mpstanalitika.pro',
            'priority': 'u=1, i',
            'referer': 'https://mpstanalitika.pro/',
            'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'x-request-id': '727e3e7c-dcd9-4849-94c0-7526cac53d04',
        }
        data = {
            "product_name": product_name,
            "length": length,
            "tone_of_voice": tone_of_voice,
            "key_words": key_words,
            "advantages": advantages,
            "minus_words": minus_words
        }
        return await self.http_session._make_request(url, method="POST", headers=headers, json=data)

    async def get_limits(self):
        url = f'{self.BASE_URL}/limits'
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': 'connect.sid=s%3AIjo0ckBExt4pvFwy7Dg0bYagizfHRpTg.uI9Jo32aDht%2F5WUj%2BNQayzvqctEpk1DwmmQVAZJJPaI; _mpsuid=531de0502eb48c4c0511f724d3d059f1',
            'if-none-match': 'W/"19-46frGdW75mYxKjN13mrFl1CtROA"',
            'priority': 'u=1, i',
            'referer': 'https://mpstanalitika.pro/',
            'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'x-request-id': 'bbbb27b3-2cf4-49e0-9d1f-b8d7f340b982'
        }
        return await self.http_session._make_request(url, headers=headers)
    

mpstats = MPStats