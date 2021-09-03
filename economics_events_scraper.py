from bs4 import BeautifulSoup

import urllib.request

class ForexFactoryScraper:

    def __init__(self, month_select):
        self._url = 'https://www.forexfactory.com/calendar.php?month=' + month_select

    def _extract_day(self, row_html):
        day_date = row_html.find("td", {"class": "calendar__date"}).text.strip()

        return day_date[:3], day_date[3:]

    def _extract_currency(self, row_html):
        return row_html.find("td", {"class":"calendar__currency"}).text.strip()

    def _extract_event(self, row_html):
        return row_html.find("td", {"class":"calendar__event"}).text.strip()

    def _extract_time(self, row_html):
        return row_html.find("td", {"class":"calendar__time"}).text.strip()

    def _extract_impact(self, row_html):
        return row_html.find("td", {"class":"impact"}).find("span").get("class")[0]

    def _extract_html_data(self):

        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        response = opener.open(self._url)
        result = response.read().decode('utf-8', errors='replace')

        return BeautifulSoup(result,"html.parser")

    def begin_extraction(self):
        parsed_html = self._extract_html_data()
        table = parsed_html.find_all("tr", class_="calendar_row")

        economic_events_dict = {}

        current_extracted_day = current_extracted_date = None
        current_time = None
        
        for row in table:
            
            # Recurring day and date is blank
            day, date = self._extract_day(row)
            current_extracted_day = day or current_extracted_day
            current_extracted_date = date or current_extracted_date

            # Events at the same time is blank
            time = self._extract_time(row)
            current_time = time or current_time

            currency = self._extract_currency(row)

            # Sometimes there are no events. This can be checked via the currency
            if not currency:
                continue

            event = self._extract_event(row)
            impact = self._extract_impact(row)

            #print("\n\n")
            print(current_extracted_date)
            print(current_extracted_day)
            print(current_time)
            print(currency)
            print(event)
            print(impact)
            print("\n\n")
            #print("\n\n")
            #print("\n\n")

ff_scraper = ForexFactoryScraper('this')
ff_scraper.begin_extraction()