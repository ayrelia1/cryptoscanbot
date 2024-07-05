import requests
import json
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from lxml import etree
import clipboard

def get_user_browser():
    chrome_driver_path = Service('ozonreviews2/chromedriver/chromedriver.exe')
    options = ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--start-maximized")
    options.add_argument("--enable-javascript")
    #options.add_argument(f'--profile-directory={profile}')
    options.add_argument("--headless=new")
    options.add_argument('--User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36')
    #options.add_argument("--no-sandbox")
    driver = Chrome(service=chrome_driver_path, options=options)
    
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        'source': '''
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_JSON;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object;
        '''
    })
    return driver

url = 'https://tonviewer.com/EQBsFm2LOjkss9BQWrbUB51qXLdWFYTQmC562-vNbE8VbdOK'

import re

driver = get_user_browser()

driver.get(url)
time.sleep(4)
html = driver.page_source

element = driver.find_element(By.XPATH, """//*[@id="__next"]/div/div[3]/div/div[1]/div[2]/div[1]/div/div/div/div[1]/div[4]/div[1]/div/div[1]/div[2]/div[1]""")
element.click()

time.sleep(1)

element = driver.find_element(By.XPATH, """//*[@id="__next"]/div[2]/div/div[2]/div/div/div[3]/div""")
element.click()

combined_text = clipboard.paste()
print(combined_text)
driver.quit()
json_text = json.loads(combined_text)
desc = json_text['description']


telegram_pattern = re.compile(r'https?://(?:t(?:elegram)?\.me|telegram\.me|t\.co)/[^\s]+')

telegram_links = telegram_pattern.findall(desc)




# Регулярное выражение для извлечения ссылок на вебсайт

website_pattern = re.compile(r"https?://(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}(?:/[a-zA-Z0-9-._~:/?#[\]@!$&'()*+,;=]*)?")

# Извлекаем ссылку на сайт из текста
website_link = None
matches = website_pattern.findall(desc)
for link in matches:
    if 'twitter' not in link and 't.me' not in link and 'x.com' not in link and 't.co' not in link:
        website_link = link
        break


dict_result = {
    "name": json_text['name'],
    "symbol": json_text['symbol'],
    "image": json_text['image'],
    "telegram": telegram_links[0],
    "website": website_link
}

print(dict_result)