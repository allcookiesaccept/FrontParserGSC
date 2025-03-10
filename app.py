import json
import time
from utils.browser import Browser
from utils.parser import GSCPageObjectManager
from utils.encoder import URLHandler
from utils.dataframes import DataProcessor
from utils.settings import Config
from utils.logger import logger

class GSCParser:
    def __init__(self, manual_login=True):
        self.config = Config()
        self.browser = Browser()
        self.parser = GSCPageObjectManager(self.browser.get_driver())
        self.data_processor = DataProcessor()
        self.url_handler = URLHandler()
        self.manual_login = manual_login
        self.results = []

    def load_urls(self):
        try:
            with open(self.config.URLS_FILE, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip()]
            logger.info(f"Loaded {len(urls)} URLs from {self.config.URLS_FILE}")
            return urls
        except Exception as e:
            logger.error(f"Failed to load URLs: {str(e)}")
            raise

    def save_url_mapping(self, urls):
        url_mapping = {url: self.url_handler.generate_gsc_url(url) for url in urls}
        try:
            with open('url_mapping.json', 'w', encoding='utf-8') as f:
                json.dump(url_mapping, f, ensure_ascii=False, indent=4)
            logger.info("URL mapping saved to url_mapping.json")
            return url_mapping
        except Exception as e:
            logger.error(f"Failed to save URL mapping: {str(e)}")
            raise

    def login(self):
        if self.manual_login:
            logger.info("Manual login enabled. Please log in within 60 seconds.")
            self.parser.login_page.open()
            time.sleep(60)  # Время на ручной ввод
        else:
            try:
                self.parser.perform_login(self.config.CREDENTIALS)
                time.sleep(5)  # Даем время на загрузку после логина
            except Exception as e:
                logger.error(f"Login failed: {str(e)}")
                raise

    def parse_urls(self, url_mapping):
        for original_url, encoded_url in url_mapping.items():
            try:

                metrics = self.parser.parse_url_metrics(encoded_url)

                metrics['url'] = original_url
                self.results.append(metrics)
                logger.info(f"Parsed metrics for {original_url}: {metrics}")
                time.sleep(10)
            except Exception as e:
                logger.warning(f"Failed to parse {original_url}: {str(e)}")
                self.results.append({
                    'url': original_url,
                    'clicks': 'N/A',
                    'impressions': 'N/A',
                    'ctr': 'N/A',
                    'positions': 'N/A'
                })
        return self.results

    def run(self):
        try:
            urls = self.load_urls()
            url_mapping = self.save_url_mapping(urls)
            self.login()
            self.parse_urls(url_mapping)
            self.data_processor.save_to_excel(self.results)
        except Exception as e:
            logger.error(f"Script failed: {str(e)}")
        finally:
            self.browser.quit()
            logger.info("Browser closed")

if __name__ == "__main__":
    parser = GSCParser(manual_login=True)
    parser.run()