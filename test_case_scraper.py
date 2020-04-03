import requests
import re
import json
import os
import django

def sync_data():
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coronavirus_county_stats.settings')
        django.setup()
        from county.models import State
        contents = requests.get('https://covidtracking.com/api/states')
        list = json.loads(contents.content)

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


        for state in list:
            print(state['state'], state['positive'], state['negative'])
            try:
                state_object = State.objects.filter(name__icontains=states[state['state']])[0]

                if state['hospitalizedCumulative'] == None and state['hospitalizedCurrently'] == None:
                    state_object.set_positive_negative_hospitalized(state['positive'], state['negative'], -1)
                    print(state['state'], 'does not have a hospitalizedCumulative value')
                elif state['hospitalizedCumulative'] != None:    
                    state_object.set_positive_negative_hospitalized(state['positive'], state['negative'], state['hospitalizedCumulative'])
                elif state['hospitalizedCurrently'] != None:
                    state_object.set_positive_negative_hospitalized(state['positive'], state['negative'], state['hospitalizedCurrently'])
            except:
                print(state['state'], 'not found!')
sync_data()