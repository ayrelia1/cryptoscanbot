from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Chrome, ChromeOptions
from config import current_directory

def get_user_browser():
    chrome_driver_path = Service('parsers/webdriver/chromedriver/chromedriver')
    options = ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--start-maximized")
    options.add_argument("--enable-javascript")
    #options.add_argument(f'--profile-directory={profile}')
    options.add_argument("--headless=new")
    options.add_argument('--User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36')
    options.add_argument("--no-sandbox")
    options.add_argument("disable-dev-shm-usage")
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