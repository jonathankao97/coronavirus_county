import json
import os
import django
import re


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coronavirus_county_stats.settings')
django.setup()
from county.models import County, State


file = open('datajsonShort.json', 'r')
dict = json.loads(file.readline())['data']['data']
day_dict = {

}

states = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AS': 'American Samoa',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'GU': 'Guam',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MP': 'Northern Mariana Islands',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NA': 'National',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'PR': 'Puerto Rico',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VI': 'Virgin Islands',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
        }


def helper(initial_list, add):
    initial_list.append(add)
    return initial_list

def next_date(month, day):
    if month == 1:
        if day == 31:
            month = 2
            day = 1
        else:
            day += 1
    elif month == 2:
        if day == 29:
            month = 3
            day = 1
        else: 
            day += 1
    else:
        day += 1
    return str(month) + "/" + str(day)


counter = 0

next_day = "1/20"

# while True:
#     if next_day == "3/23":
#         break
#     next_day = next_date(int(re.split("/", next_day)[0]), int(re.split("/", next_day)[1]))
#     print(next_day)
# SETUP DAY_DICT
for item in dict:
    if item['confirmed_date'] != "3/23":
        if item['confirmed_date'] in day_dict:
            day_dict[item["confirmed_date"]].append([item['state_name'], item['county'], item['people_count'], item['die']])
        else:
            day_dict[item['confirmed_date']] = [[item['state_name'], item['county'], item['people_count'], item['die']]]

#RESET ALL LISTS

for county in County.objects.all():
    county.set_deaths([])
    county.set_confirmed([])
    county.set_state_county_ranking([])


length_counter = 0
while True:
    length_counter += 1
    if next_day == "3/23":
        break

    if next_day in day_dict:
        list = day_dict[next_day]
        # REPORT SYNTAX: [STATE, COUNTY, CONFIRMED, DEATHS]
        for report in list:
            try:
                state = State.objects.filter(name=states[report[0]])[0]
                print(state.name)
                county = County.objects.filter(name=report[1])[0]
                print(county.name)
                if len(county.get_confirmed()) == length_counter:
                    confirmed_list = county.get_confirmed()
                    dead_list = county.get_deaths()
                    confirmed_list[-1] += report[2]
                    dead_list[-1] += report[3]
                    county.set_confirmed(confirmed_list)
                    county.set_deaths(dead_list)
                else:
                    county.set_confirmed(helper(county.get_confirmed(), county.get_confirmed()[-1] + report[2]))
                    county.set_deaths(helper(county.get_deaths(), county.get_deaths()[-1] + report[3]))
            except:
                print(report, "BROKE")

        for county in County.objects.all():
            confirmed_list = county.get_confirmed()
            if len(confirmed_list) != length_counter:
                county.set_confirmed(helper(county.get_confirmed(), county.get_confirmed()[-1]))
                county.set_deaths(helper(county.get_deaths(), county.get_deaths()[-1]))
    #     add to list
    else:
        for county in County.objects.all():
            confirmed_list = county.get_confirmed()
            dead_list = county.get_deaths()
            if len(confirmed_list) == 0:
                confirmed_list.append(0)
                dead_list.append(0)
            else:
                confirmed_list.append(confirmed_list[-1])
                dead_list.append(dead_list[-1])
            county.set_confirmed(confirmed_list)
            county.set_deaths(dead_list)

    print(next_day, "has been processed")
    next_day = next_date(int(re.split("/", next_day)[0]), int(re.split("/", next_day)[1]))

    # list.append(item['fulldate'])
    # print(item['people_count'], item['county'], item['state_name'])

# print(dict)
# print(list)

# del list
# print(daily_seen_dict)
print(counter)
file.close()
del dict
# del daily_seen_dict
