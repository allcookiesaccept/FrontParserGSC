
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import Logger
from utils.encoder import URLHandler

class LoginPage:
    URL = 'https://accounts.google.com/signin'

    # Локаторы элементов
    __email_field = (By.ID, 'identifierId')
    __next_button = (By.ID, 'identifierNext')
    __password_field = (By.NAME, 'password')
    __password_next = (By.ID, 'passwordNext')

    def __init__(self, browser):
        self.browser = browser
        self.driver = browser.
        self.logger = Logger().get_logger()
        self.wait = WebDriverWait(driver, 20)

    def open(self):
        self.driver.get(self.URL)
        return self

    def enter_email(self, email):
        email_input = self.wait.until(EC.element_to_be_clickable(self.__email_field))
        email_input.clear()
        email_input.send_keys(email)
        return self

    def click_next(self):
        self.wait.until(EC.element_to_be_clickable(self.__next_button)).click()
        return self

    def enter_password(self, password):
        password_input = self.wait.until(EC.element_to_be_clickable(self.__password_field))
        password_input.clear()
        password_input.send_keys(password)
        return self

    def submit_login(self):
        self.wait.until(EC.element_to_be_clickable(self.__password_next)).click()
        self.logger.info("Login form submitted")
        return self


class PerformanceReportPage:
    # Локаторы метрик
    __metrics = {
        'clicks': (By.CSS_SELECTOR, 'div[data-guidedhelpid="scorecard_0"] div.nnLLaf.vtZz6e'),
        'impressions': (By.CSS_SELECTOR, 'div[data-guidedhelpid="scorecard_1"] div.nnLLaf.vtZz6e'),
        'ctr': (By.CSS_SELECTOR, 'div[data-guidedhelpid="scorecard_2"] div.nnLLaf.vtZz6e'),
        'positions': (By.CSS_SELECTOR, 'div[data-guidedhelpid="scorecard_3"] div.nnLLaf.vtZz6e')
    }

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.logger = Logger().get_logger()

    def load_report(self, url):
        self.driver.get(url)
        self.logger.info(f"Report loaded: {url}")
        return self

    def get_metric(self, metric_name):
        locator = self.__metrics.get(metric_name)
        if not locator:
            self.logger.error(f"Unknown metric: {metric_name}")
            return 'N/A'

        try:
            return self.wait.until(EC.presence_of_element_located(locator)).text.strip()
        except:
            self.logger.warning(f"Metric {metric_name} not found")
            return 'N/A'


class GSCPageObjectManager:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.report_page = PerformanceReportPage(driver)

    def perform_login(self, credentials):
        self.login_page.open() \
            .enter_email(credentials['email']) \
            .click_next() \
            .enter_password(credentials['password']) \
            .submit_login()
        return self

    def parse_url_metrics(self, original_url):
        gsc_url = URLHandler.generate_gsc_url(original_url)
        self.report_page.load_report(gsc_url)

        return {
            'url': original_url,
            'clicks': self.report_page.get_metric('clicks'),
            'impressions': self.report_page.get_metric('impressions'),
            'ctr': self.report_page.get_metric('ctr'),
            'positions': self.report_page.get_metric('positions')
        }