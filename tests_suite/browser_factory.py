from selenium import webdriver
from configparser import ConfigParser

config = ConfigParser()
config.read('config/config.ini')
print("Available config sections:", config.sections())
print("Available options in DEFAULT:", config.defaults())

class browser_factory:
    @staticmethod
    def get_driver():
        browser = config.get('DEFAULT', 'BROWSER', fallback='chrome')
        
        if browser.lower() == 'chrome':
            options = webdriver.ChromeOptions()
            if config.getboolean('DEFAULT', 'HEADLESS'):
                options.add_argument("--headless=new")
            return webdriver.Chrome(options=options)
            
        elif browser.lower() == 'firefox':
            return webdriver.Firefox()
            
        else:
            raise ValueError(f"Unsupported browser: {browser}")