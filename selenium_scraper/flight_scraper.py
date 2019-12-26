from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import datetime

# Edit Chrome webdriver based on your installation path
PATH = "/Users/chayaphatnicrothanon/PycharmProjects/flight_expedia_scraper"
browser = webdriver.Chrome(executable_path=PATH + '/chromedriver')

# Choose ticket type
return_ticket = "//label[@id='flight-type-roundtrip-label-hp-flight']"
one_way = "//label[@id='flight-type-one-way-label-hp-flight']"
multi = "//label[//[@id='flight-type-multi-dest-label-hp-flight']]"


def ticket_chooser(ticket):
    """
    Choose flight ticket type and automatically click button
    :param ticket: a ticket type [Return, One way, Multi-City]
    :return:
    """
    try:
        # Find the ticket type's button
        ticket_type = browser.find_element_by_xpath(ticket)
        ticket_type.click()

    except Exception as e:
        print("Ticket type not found")


def departure_chooser(dep):
    """
    Choose the departure country and select the first options provided by Expedia
    Example: if the user type "BKK" -> the first item will show "Bangkok, Thailand all airports"

    Note: that we need to sleep the program for some occasions for the webpage to be fetched
    :param dep: departure country
    :return:
    """

    # Find the input box of departure
    departure_from = browser.find_element_by_xpath(
        "//input[@id='flight-origin-hp-flight']")
    time.sleep(1.5)

    # Clear the text in the box
    departure_from.clear()

    # Specify the departure country
    departure_from.send_keys(dep)
    time.sleep(2)

    # Select the first result in the list when specify departure country
    try:
        first_item = browser.find_element_by_xpath("//a[@id='aria-option-0']")
    except Exception as e:
        print("Fail to click the departure country")

    first_item.click()


def arrival_chooser(arrive):
    """
    Choose the arrival country and select the first options provided by Expedia
    :param arrive: arrival country
    :return:
    """
    # Find the input box of arrival country
    arrive_to = browser.find_element_by_xpath(
        "//input[@id='flight-destination-hp-flight']")
    time.sleep(1.5)

    # Clear the text in the box
    arrive_to.clear()

    # Specify the arrival country
    arrive_to.send_keys(arrive)
    time.sleep(2)

    # Select first result in the list
    try:
        first_item = browser.find_element_by_xpath("//a[@id='aria-option-0']")
    except Exception as e:
        print("Fail to click the arrival country")

    first_item.click()


def departure_date_picker(month, day, year):
    """
    Choose departure date

    Note: the date format may change. Current use is "MM / DD / YYYY"
    :param month:
    :param day:
    :param year:
    :return:
    Note:
    """

    # Select the input box of the departure date
    dep_date_btn = browser.find_element_by_xpath(
        "//input[@id='flight-departing-hp-flight']")
    dep_date_btn.clear()
    dep_date_btn.send_keys(month + '/' + day + '/' + year)
    time.sleep(1)


def arrival_date_picker(month, day, year):
    """
    Choose arrival date

    Note: the date format may change. Current use is "MM / DD / YYYY"
    :param month:
    :param day:
    :param year:
    :return:
    """
    # Select the input box of the arrival date
    return_date_btn = browser.find_element_by_xpath(
        "//input[@id='flight-returning-hp-flight']")
    return_date_btn.clear()
    return_date_btn.send_keys(month + '/' + day + '/' + year)
    time.sleep(1)


def search_click():
    """
    Click search button
    :return:
    """

    search_box = browser.find_element_by_xpath("//button[@class='btn-primary btn-action gcw-submit']")
    search_box.click()
    time.sleep(20)  # Quite long delay when searching ...

    print('Search button has been clicked!')


df = pd.DataFrame()


def get_all_flight():
    global df
    global dep_time_list
    global arr_time_list
    global airlines_list
    global price_list
    global durations_list
    global stops_list
    global layovers_list

    # Get departure time
    dep_time = browser.find_elements_by_xpath(
        "//span[@data-test-id='departure-time']")
    dep_time_list = [elem.text for elem in dep_time]

    # Get arrival time
    arr_time = browser.find_elements_by_xpath(
        "//span[@data-test-id='arrival-time']")
    arr_time_list = [elem.text for elem in arr_time]

    # Get airline name
    airlines = browser.find_elements_by_xpath(
        "//span[@data-test-id='airline-name']")
    airlines_list = [value.text for value in airlines]

    # Get durations
    durations = browser.find_elements_by_xpath("//span[@data-test-id='duration']")
    durations_list = [value.text for value in durations]

    # Get number_stops
    stops = browser.find_elements_by_xpath("//span[@class='number-stops']")
    stops_list = [value.text for value in stops]

    # Get prices
    prices = browser.find_elements_by_xpath(
        "//span[@data-test-id='listing-price-dollars']")
    price_list = [value.text for value in prices]

    now = datetime.datetime.now()
    current_date = (str(now.year) + '-' + str(now.month) + '-' + str(now.day))
    current_time = (str(now.hour) + ':' + str(now.minute))
    current_price = 'price' + '(' + current_date + '---' + current_time + ')'

    for i in range(len(dep_time_list)):
        try:
            df.loc[i, 'departure_time'] = dep_time_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'arrival_time'] = arr_time_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'airline'] = airlines_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'duration'] = durations_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'stops'] = stops_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, str(current_price)] = price_list[i]
        except Exception as e:
            pass

        df.to_csv('output.csv', index=False)
    print('Excel Sheet Created!')
