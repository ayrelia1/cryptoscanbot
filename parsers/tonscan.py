import asyncio
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

class Tonscan(BaseParser):
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
        async with self.get_browser() as driver:
            driver.get(f"https://tonviewer.com/{address}")
            await asyncio.sleep(4.2)
            try:
                element = driver.find_element(By.XPATH, """//*[@id="__next"]/div/div[3]/div/div[1]/div[2]/div[1]/div/div/div/div[1]/div[4]/div[1]/div/div[1]/div[2]/div[1]""")
                element.click()

                await asyncio.sleep(1)

                element = driver.find_element(By.XPATH, """//*[@id="__next"]/div[2]/div/div[2]/div/div/div[3]/div""")
            except selenium.common.exceptions.NoSuchElementException:
                return None
            element.click()

            json_info = clipboard.paste()
        return json_info
        
    async def parse_html(self, json_info: dict) -> str:

        
        decs = json_info['description']    
        
        telegram_pattern = re.compile(r'https?://(?:t(?:elegram)?\.me|telegram\.me|t\.co)/[^\s]+')
        telegram_link = self.find_links_in_text('tg', decs, telegram_pattern)
        
        website_pattern = re.compile(r"https?://(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}(?:/[a-zA-Z0-9-._~:/?#[\]@!$&'()*+,;=]*)?")
        website_link = self.find_links_in_text('site', decs, website_pattern)
             
    
        dict_result = {
            "name": json_info['name'],
            "symbol": json_info['symbol'],
            "image": json_info['image'],
            "telegram": telegram_link,
            "website": website_link
        }
    
        return dict_result
    


   

if __name__ == '__main__':
    ton = Tonscan()
    print(asyncio.run(ton.get_token_info('https://tonviewer.com/EQBsFm2LOjkss9BQWrbUB51qXLdWFYTQmC562-vNbE8VbdOK')))
        