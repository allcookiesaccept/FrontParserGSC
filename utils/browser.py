from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from utils.logger import logger

class Browser:

    By = By
    Keys = Keys

    def __init__(self):
        logger.info("Starting Webdriver")
        self.options = Options()
        self.options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
        )

    def __call__(self):
        self.driver: webdriver = webdriver.Chrome(self.options)
        self.driver.implicitly_wait(10)

    def get_driver(self):
        if not self.driver:
            self.__call__()
        return self.driver

    def quit(self):
        if self.driver:
            self.driver.quit()
            self.driver = None