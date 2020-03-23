from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import re
import os
import django
import json
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coronavirus_county_stats.settings')
django.setup()
from county.models import add_city, add_county, add_state


def parse_county(state, counter, county):
    county_info = county.find_all('span', 'jsx-314244412')
    name = county_info[0].text  # get rid of all weird extra spaces
    if name[-1] == ' ':
        name = name[0:-1]
    if len(county_info[1].find_all('div')) == 0:
        confirmed = county_info[1].text
    else:
        county_info[1].find_all('div')[0].decompose()
        confirmed = county_info[1].text
    if len(county_info[2].find_all('div')) == 0:
        deaths = county_info[2].text
    else:
        county_info[2].find_all('div')[0].decompose()
        deaths = county_info[2].text

    with open('dict.json', 'r') as file:
        dict = json.loads(file.readline())

    key = name + "," + state.name
    if key[-1] == " ":
        key = key[:-1]
    if key in dict:
        fips_code = dict.get(key)[0][1]
        county_object = add_county(name=name, fips_code=fips_code,
                                   confirmed=int(confirmed), deaths=int(deaths), county_ranking=counter+1, state=state)
        for city in dict.get(key):
            add_city(zip_code=city[1], name=city[2], county=county_object)
    else:
        print("Not in dict", key)


def parse_state(counter, state_info):
    name = state_info[0].text

    if len(state_info[1].find_all('div')) == 0:
        confirmed = state_info[1].text
    else:
        state_info[1].find_all('div')[0].decompose()
        confirmed = state_info[1].text
    if len(state_info[2].find_all('div')) == 0:
        deaths = state_info[2].text
    else:
        state_info[2].find_all('div')[0].decompose()
        deaths = state_info[2].text
    return add_state(name=name, confirmed=int(confirmed), deaths=int(deaths), state_ranking=counter+1)


def sync_data():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    # #
    browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    browser.get('https://coronavirus.1point3acres.com/en')

    # browser = webdriver.Chrome('/Users/jkao97/downloads/chromedriver')
    # # # browser = webdriver.Chrome('/Users/JonKao/downloads/chromedriver')
    # browser.get('https://coronavirus.1point3acres.com/en')

    # print(browser.page_source)

    sleep(3)
    counter = 0
    for state in browser.find_elements_by_xpath("//div[(@class = 'jsx-314244412')]"):
        if state.get_attribute("class") == 'jsx-314244412':
            counter = 0
            try:
                print("trying")
                state.click()
            except:
                print("failing", counter)
                counter += 1
                browser.execute_script('scrollBy(0, 100)')
                state.click()
    soup = BeautifulSoup(browser.page_source, "lxml")
    for index, state in enumerate(soup.find_all(lambda tag: tag.name == 'div' and
                                       tag.get('class') == ['jsx-314244412'])):
        state_info = state.find('div', 'jsx-314244412 stat row expand').find_all('span', 'jsx-314244412')
        state_object = parse_state(index, state_info)  # add state
        counties_list = state.find('div', 'jsx-314244412 counties')
        for index2, county in enumerate(counties_list.find_all('div', 'jsx-314244412 row')):
            parse_county(state_object, index2, county)  # add all counties/cities

sync_data()
