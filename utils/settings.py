import os
from dotenv import load_dotenv
from pathlib import Path

class Config:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance


    def _load_config(self):
        load_dotenv()
        self.BASE_DIR = Path(os.getenv("BASE_DIR", Path(__file__).resolve().parent.parent))
        self.CREDENTIALS = {
            'email': os.getenv('USER'),
            'password': os.getenv('PASSWORD')
        }
        self.URLS_FILE = os.path.join(self.BASE_DIR, 'urls.txt')
        self.OUTPUT_FILE = os.path.join(self.BASE_DIR, 'gsc_data.xlsx')
