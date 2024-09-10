import asyncio
from lxml import etree
from bs4 import BeautifulSoup
from parsers.baseparser import BaseParser
import re

class Etherscan(BaseParser):
    def __init__(self):
        pass
    
    @staticmethod
    def get_headers():
        return {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }
        
    async def get_token_info(self, url: str) -> dict:
        html_page = await self.get_html_page(url)
        result = await self.parse_html(html_page)
        return result
        
        
    async def get_html_page(self, address: str) -> str:
        async with self.get_browser() as driver:
            driver.get(f"https://etherscan.io/address/{address}#code")
            await asyncio.sleep(4.2)
            html_page = driver.page_source
        return html_page
        
    async def parse_html(self, html_page: str) -> str:
        soup = BeautifulSoup(html_page, 'html.parser')
        # Инициализируем BeautifulSoup
        ace_lines = soup.find_all(class_="ace_line")

        # Собираем первые 20 строк из каждого блока в одну переменную
        combined_text = ""
        for ace_line in ace_lines:
            combined_text += ace_line.text.strip() + "\n"
            
        print(combined_text)
        
        telegram_pattern = re.compile(r'https?://(?:t(?:elegram)?\.me|telegram\.me|t\.co)/[^\s]+')
        telegram_link = self.find_links_in_text('tg', combined_text, telegram_pattern)
        
        website_pattern = re.compile(r"https?://(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}(?:/[a-zA-Z0-9-._~:/?#[\]@!$&'()*+,;=]*)?")
        website_link = self.find_links_in_text('site', combined_text, website_pattern)
                  
        token_block = soup.find('div', class_='d-flex align-items-center gap-1 mt-2')
        
        name, symbol = None, None
        if token_block:
            # Извлечение текста из элемента 'a'
            token_text = token_block.find('a').get_text()
            
            # Разделение текста на название и символ
            name, symbol = token_text.split(' (')
            symbol = symbol.rstrip(')')  # Удаление закрывающей скобки из символа    
    
        dict_result = {
            "name": name,
            "symbol": symbol,
            "image": None,
            "telegram": telegram_link,
            "website": website_link
        }
        return dict_result
    
      

if __name__ == '__main__':
    eth = Etherscan()
    print(asyncio.run(eth.get_token_info('https://etherscan.io/address/0xB5aEBDbf87e3429d6bDF3cedB40A7E3D23F8e200#code')))
        
        
        
        