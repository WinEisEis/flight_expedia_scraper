from selenium_scraper import flight_scraper
import time

link = 'https://www.expedia.com/'


def execute_flight_scraper():
    flight_scraper.browser.get(link)
    time.sleep(5)

    # Choose flights only
    flights_only = flight_scraper.browser.find_element_by_xpath("//button[@id='tab-flight-tab-hp']")
    flights_only.click()

    flight_scraper.ticket_chooser(flight_scraper.return_ticket)
    flight_scraper.departure_chooser('Bangkok')
    flight_scraper.arrival_chooser('Taiwan')
    flight_scraper.departure_date_picker('04', '12', '2020')
    flight_scraper.arrival_date_picker('04', '16', '2020')
    flight_scraper.search_click()
    flight_scraper.get_all_flight()
