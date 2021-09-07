from bs4 import BeautifulSoup
from datetime import datetime

import pandas as pd
import urllib.request

class ForexFactoryScraper:

    def __init__(self, month_select):
        self._url = 'https://www.forexfactory.com/calendar.php?month=' + month_select
        self._extracted_events = None

        self._begin_extraction()

    def _extract_day(self, row_html):
        day_date = row_html.find("td", {"class": "calendar__date"}).text.strip()
        return day_date[3:]

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

    def _begin_extraction(self):
        parsed_html = self._extract_html_data()
        table = parsed_html.find_all("tr", class_="calendar_row")

        economic_events_list = []

        current_extracted_date = None
        current_time = None
        
        for row in table:

            currency = self._extract_currency(row)

            # Sometimes there are no events. This can be checked via the currency
            if not currency:
                continue
            
            # Recurring day and date is blank
            current_extracted_date = self._extract_day(row) or current_extracted_date

            # Events at the same time is blank
            current_time = self._extract_time(row) or current_time

            event = self._extract_event(row)
            impact = self._extract_impact(row)

            economic_events_list.append({
                'date': current_extracted_date,
                'time_minus_12hours': current_time,
                'currency': currency,
                'event': event,
                'impact': impact
            })
        
        events_df = pd.DataFrame(economic_events_list)
        events_df['impact'] = events_df.impact.map({'high': 1, 'medium': 2, 'low': 3}).fillna(4).astype(int)

        self._extracted_events = events_df

        return None

    def get_today_events(self):

        # Remove leading 0 from date.
        # If using non-windows, replace '#' with '-'
        current_date = datetime.now().strftime("%b %#d")
        extracted_events_copy = self._extracted_events.copy()

        filtered_events = extracted_events_copy[extracted_events_copy['date'] == current_date]
        filtered_events = filtered_events.groupby('currency')

        for currency, frame in filtered_events:
            print(f"{currency}\n")

            for index, row in frame.iterrows():
                print(f"{row['event']} at {row['time_minus_12hours']}.\nImpact: {row['impact']}\n")

            print("\n\n-----\n\n")

        return None

ff_scraper = ForexFactoryScraper('this')

today_events = ff_scraper.get_today_events()