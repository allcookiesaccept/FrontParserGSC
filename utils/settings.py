import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.DRIVER_PATH = os.getenv('DRIVER_PATH', 'chromedriver')
        self.CREDENTIALS = {
            'email': os.getenv('GSC_EMAIL'),
            'password': os.getenv('GSC_PASSWORD')
        }
        self.URLS_FILE = os.path.join(self.BASE_DIR, 'urls.txt')
        self.OUTPUT_FILE = os.path.join(self.BASE_DIR, 'gsc_data.xlsx')
        self.LOG_FILE = os.path.join(self.BASE_DIR, 'gsc_scraper.log')