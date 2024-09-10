from abc import ABC, abstractmethod
import asyncio
from parsers.webdriver.webdriver import get_user_browser
from contextlib import asynccontextmanager
import re
import xvfbwrapper
vdisplay = xvfbwrapper.Xvfb(width=1920, height=1080)

class BaseParser(ABC):
    
    @asynccontextmanager
    async def get_browser(self):
        vdisplay.start()
        
        driver = get_user_browser()
        try:
            yield driver
        finally:
            vdisplay.stop()
            driver.quit()
    
    @staticmethod
    @abstractmethod
    def get_headers():
        raise NotImplementedError
    
    @abstractmethod
    async def get_token_info(self):
        raise NotImplementedError
    
    @abstractmethod
    async def get_html_page(self):
        raise NotImplementedError
    
    @abstractmethod
    async def parse_html(self):
        raise NotImplementedError

    
    # поиск прямо в текст 
    @staticmethod
    def find_links_in_text(typee, text, pattern: re):
        if typee == 'tg':
            telegram_links = pattern.findall(text)
            if telegram_links:
                return telegram_links[0]
            return None
        elif typee == "site":
            website_link = None
            matches = pattern.findall(text)
            for link in matches:
                if 'twitter' not in link and 't.me' not in link and 'x.com' not in link and 't.co' not in link and 'discord.com' not in link and 'whitepaper.io' not in link:
                    website_link = link
                    break
            return website_link
    
