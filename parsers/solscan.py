import asyncio
from lxml import etree
from bs4 import BeautifulSoup
import aiohttp
from parsers.baseparser import BaseParser
import re
import logging
from contextlib import asynccontextmanager

class Solscan(BaseParser):
    def __init__(self):
        pass
    
    @staticmethod
    def get_headers():
        return {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }
        
    async def get_token_info(self, url: str) -> dict:
        html_page = await self.get_html_page(url)
        uri_ipfs = await self.parse_html(html_page)
        if uri_ipfs:
            token_info = await self.parse_uri(uri_ipfs)
            return token_info
        return {}
        
        
    
    async def get_html_page(self, address: str) -> str:
        async with self.get_browser() as driver:
            driver.get(f"https://solscan.io/token/{address}#metadata")
            await asyncio.sleep(4.2)
            html_page = driver.page_source
        return html_page
        
    async def parse_html(self, html_page: str) -> str:
        soup = BeautifulSoup(html_page, 'html.parser')
        html_str = str(soup)
        tree = etree.HTML(html_str)
        uri_element = tree.xpath('//*[@id="radix-:rk:-content-json"]/div/div/div/div/div/div/div/div[4]/div/div/div[3]/div/div/span')
        if uri_element:
            print('uri finded')
            uri = uri_element[0].text 
            uri_ipfs = uri[1:-1]
            return uri_ipfs
        return None
        
        
    async def parse_uri(self, uri_ipfs: str) -> dict:
        async with aiohttp.ClientSession(headers=self.get_headers()) as session:
            async with session.get(uri_ipfs) as response:
                result = await response.json()
        
        
        desc = result.get('description', '')
        
        result_find = self.find_keys(result, ["website", "telegram", "site"])
        
        if not result_find['telegram']:
            # функции поиска прямо в тексте
            telegram_pattern = re.compile(r'https?://t(?:elegram)?\.(?:me|co|org)[^\s]+')
            telegram_link = self.find_links_in_text('tg', desc, telegram_pattern)
            
            if telegram_link:
                result_find['telegram'] = telegram_link

        website = result_find['website'] or result_find['site']

        image = result.get('image', None)
        print(image)
        if image and 'cf-ipfs.com' in image:
            image = image.replace('cf-ipfs.com', 'ipfs.io')
        print(image)
        dict_result = {
            "name": result.get('name', None),
            "symbol": result.get('symbol', None),
            "image": image,
            "telegram": result_find['telegram'],
            "website": website
        }
        print(dict_result)
        return dict_result
    
    @staticmethod
    def find_keys(d, keys_to_find):
        found_keys = {key: None for key in keys_to_find}

        def recursive_search(current_dict):
            for key, value in current_dict.items():
                if key in found_keys:
                    found_keys[key] = value
                elif isinstance(value, dict):
                    recursive_search(value)

        recursive_search(d)
        return found_keys


   

if __name__ == '__main__':
    sol = Solscan()
    print(asyncio.run(sol.get_token_info('https://solscan.io/token/2FjS6rETovPLvQ8CSxeZmopnhrRCtdxEM94i1h3gpump#metadata')))
        
        
        
        