from bs4 import BeautifulSoup

import urllib.request

class ForexFactoryScraper:

    def __init__(self, month_select):
        self._url = 'https://www.forexfactory.com/calendar.php?month=' + month_select

    def _extract_day(self, row_html):
        day_date = row_html.find("td", {"class": "calendar__date"}).text.strip()

        return day_date[:3], day_date[3:]

    def _extract_html_data(self):

        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        response = opener.open(self._url)
        result = response.read().decode('utf-8', errors='replace')

        return BeautifulSoup(result,"html.parser")

    def begin_extraction(self):
        parsed_html = self._extract_html_data()
        table = parsed_html.find_all("tr", class_="calendar_row")
        
        for index,item in enumerate(table):
            
            day, date = self._extract_day(item)
            currency = item.find_all("td", {"class":"calendar__currency"})
            event = item.find_all("td",{"class":"calendar__event"})
            time = item.find_all("td", {"class":"calendar__time"})
            impact = item.find_all("td", {"class":"impact"})

            if day in ['Sat', 'Sun']:
                continue

            #print("\n\n")
            #print(currency)
            #print("\n\n")
            #print(event)
            #print("\n\n")
            #print(time)
            #print("\n\n")
            #print(impact)

ff_scraper = ForexFactoryScraper('this')
ff_scraper.begin_extraction()