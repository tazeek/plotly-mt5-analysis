from bs4 import BeautifulSoup

import requests

class ForexFactoryScraper:

    def __init__(self, month_select):
        self._url = 'https://www.forexfactory.com/calendar?month=' + month_select

    def extract_html_data(self):
        response = requests.get(self._url)
        data = response.text
        soup = BeautifulSoup(data, 'lxml')

    def begin_extraction(self):
        ...

ff_scraper = ForexFactoryScraper('this')
ff_scraper.extract_html_data()