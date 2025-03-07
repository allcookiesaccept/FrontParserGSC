from urllib.parse import quote
from settings import Config


class URLHandler:
    @staticmethod
    def encode_url(original_url):
        return quote(original_url, safe=':/')

    @staticmethod
    def generate_gsc_url(original_url):
        base_url = ("https://search.google.com/search-console/performance/search-analytics?"
                    "resource_id=https%3A%2F%2Fbetonmobile.ru%2F&"
                    "metrics=CLICKS%2CIMPRESSIONS%2CCTR%2CPOSITION&"
                    "num_of_days=28&country=rus&page=!")

        return base_url + URLHandler.encode_url(original_url)