from bs4 import BeautifulSoup

import urllib.request

class ForexFactoryScraper:

    def __init__(self, month_select):
        self._url = 'https://www.forexfactory.com/calendar.php?month=' + month_select

    def _extract_html_data(self):

        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        response = opener.open(self._url)
        result = response.read().decode('utf-8', errors='replace')

        return BeautifulSoup(result,"html.parser")

    def begin_extraction(self):
        parsed_html = self._extract_html_data()
        table = parsed_html.find_all("tr", class_="calendar_row")
        
        for item in table:
            
            date = item.find_all("td", {"class": "calendar__date"})
            currency = item.find_all("td", {"class":"calendar__currency"})
            event = item.find_all("td",{"class":"calendar__event"})
            time = item.find_all("td", {"class":"calendar__time"})
            impact = item.find_all("td", {"class":"impact"})

            print("\n\n")
            print(date)
            print("\n\n")
            print(currency)
            print("\n\n")
            print(event)
            print("\n\n")
            print(time)
            print("\n\n")
            print(impact)
            break

ff_scraper = ForexFactoryScraper('this')
ff_scraper.begin_extraction()