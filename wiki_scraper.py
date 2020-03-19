from bs4 import BeautifulSoup
import requests
import json

r = requests.get("https://en.wikipedia.org/wiki/List_of_U.S._municipalities_in_multiple_counties")
soup = BeautifulSoup(r.content, 'lxml')

table_list = soup.find_all('table', class_='wikitable')

with open('dict.json', 'r') as file:
    dict = json.loads(file.readline())
    for table in table_list:
        tr_list = table.find_all('tr')
        for tr in tr_list:
            td_list = tr.find_all('td')
            if len(td_list) != 0:
                if len(td_list[0].find_all('a')) != 0:
                    city = td_list[0].a.text
                    county_list = td_list[-1].find_all('a')
                    # text_list = []
                    for county in county_list:
                        if county in dict:
                            if city in dict.get(county):
                                print("CITY already accounted for")
                            else:
                                pass
                        else:
                            print("County not in DICT")
                    # for item in county_list:
                    #     text_list.append(item.text)
                    print(city, text_list)
