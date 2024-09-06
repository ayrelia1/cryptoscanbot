import asyncio
from typing import List
from lxml import etree
from bs4 import BeautifulSoup
import selenium.common
from parsers.baseparser import BaseParser
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import clipboard
import json
import selenium
import aiohttp

class Tronscan(BaseParser):
    def __init__(self):
        pass
    
    @staticmethod
    def get_headers():
        return {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }
        
    async def get_token_info(self, url: str) -> dict:
        json_info = await self.get_html_page(url)
        if json_info:
            result = await self.parse_html(json.loads(json_info))
            return result
        return {}
        
        
    async def get_html_page(self, address: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=f"https://apilist.tronscanapi.com/api/token_trc20?contract={address}&showAll=1&start=&limit=") as resp:
                try: 
                    resp_json = await resp.json()
                except:
                    return None
        await self.parse_html(resp_json)
        
    async def parse_html(self, json_info: dict) -> str:
        telegram_link = None
        twitter_link = None
        
        
        
        token: dict = json_info['trc20_tokens'][0]    
        social_media_list: List[dict] = token.get('social_media_list', {})
        
        for media in social_media_list:
            if media['name'] == 'Telegram':
                telegram_link = media["url"]
                telegram_link = json.loads(telegram_link)


        website_link = token.get('home_page', None)    
        
        print(json_info)
        print(token)
        
        dict_result = {
            "name": token['name'],
            "symbol": token['symbol'],
            "image": token['icon_url'],
            "telegram": telegram_link,
            "website": website_link
        }
    
        return dict_result
    


   

if __name__ == '__main__':
    ton = Tronscan()
    print(asyncio.run(ton.get_token_info('TZ5dAbT4xTsRDfvGQeRGVLwXvzGaydKzpR')))
        