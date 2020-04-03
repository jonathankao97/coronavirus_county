import json
import os
import requests
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coronavirus_county_stats.settings')
django.setup()
from county.models import County, State

contents = requests.get('https://covidtracking.com/api/states/daily')
list = json.loads(contents.content)

date_dict = {
	
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
    print("month", month, "day", day)
    if month == "01":
        if day == "31":
            month = 2
            day = 1
        else:
            day = int(day)
            day += 1
    elif month == "02":
        if day == "29":
            month = 3
            day = 1
        else: 
            day = int(day)
            day += 1
    elif month == "03":
    	if day == "31":
    		month = 4
    		day = 1
    	else:
    		day = int(day)
    		day += 1
    else:
        day = int(day)
        day += 1
    if int(month) < 10 and len(str(month)) < 2:
        month = "0" + str(month)
    if int(day) < 10 and len(str(day)) < 2:
        day = "0" + str(day)
    return "2020" + str(month) + str(day)


for item in list:
	if item["date"] in date_dict:
		date_dict[item["date"]].append(item)
	else:
		date_dict[item["date"]] = [item]

for state in State.objects.all():
	state.set_past_positive([])
	state.set_past_negative([])
	state.set_hospitalized([])

next_day = "20200120"

length_counter = 0
while True:
	length_counter += 1
	if next_day == "20200402":
		break
	if int(next_day) in date_dict:
		for item in date_dict[int(next_day)]:
			try:
				state_object = State.objects.filter(name=states[item["state"]])[0]
				state_object.set_past_positive(helper(state_object.get_past_positive(), item["positive"]))
				state_object.set_past_negative(helper(state_object.get_past_negative(), item["negative"]))
				state_object.set_hospitalized(helper(state_object.get_hospitalized(), item["hospitalized"]))
			except:
				print(item["state"], "NOT FOUND!")
	else:
		for state in State.objects.all():
			state.set_past_positive(helper(state.get_past_positive(), 0))
			state.set_past_negative(helper(state.get_past_negative(), 0))
			state.set_hospitalized(helper(state.get_hospitalized(), 0))
	print(next_day, "has been processed")
	next_day = next_date(next_day[4:6], next_day[6:])
