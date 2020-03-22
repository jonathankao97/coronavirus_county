from django.shortcuts import render
from county.models import City, County, State
from django.utils import timezone
from datetime import timedelta

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands': 'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Palau': 'PW',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}


def mail(request):
    return render(request, 'material-design-email-template/material-design-email-template/material-design.html')


def test(request):
    return render(request, 'test.html')


def hello(request):
    return render(request, 'hello.html')


def data(request, county_id):
    sups = ["aux", "st", "nd", "rd", "th"]
    county = County.objects.get(id=county_id)
    confirmed = day_array_converter(county.get_confirmed(), 30)
    confirmed_delta = 0
    if len(confirmed) > 1:
        confirmed_delta = confirmed[-1] - confirmed[-2]
    confirmed_increase = 0
    if len(confirmed) >= 2 and confirmed[-2] != 0:
        confirmed_increase = int(float(confirmed_delta * 100) / confirmed[-2])
    deaths = day_array_converter(county.get_deaths(), 30)
    deaths_delta = 0
    if len(deaths) > 1:
        deaths_delta = deaths[-1] - deaths[-2]
    deaths_increase = 0
    if len(deaths) >= 2 and deaths[-2] != 0:
        deaths_increase = int(float(deaths_increase * 100) / deaths[-2])
    county_rank = int(county.get_state_county_ranking()[-1])
    state_rank = int(county.state.get_state_ranking()[-1])
    context = {
        'confirmed': confirmed,
        'confirmed_delta': confirmed_delta,
        'confirmed_increase': confirmed_increase,
        'deaths': deaths,
        'deaths_delta': deaths_delta,
        'death_increase': deaths_increase,
        'county_rank': county_rank,
        'county_rank_sup': sups[min(4, county_rank)],
        'state_rank': state_rank,
        'state_rank_sup': sups[min(4, state_rank)],
        'county': county,
        'state': county.state,
        'x_axis': []
    }
    now = timezone.localtime(timezone.now())
    for i in range(0, min(len(confirmed), 30)):
        context['x_axis'].append(now.strftime('%-m/%-d'))
        now -= timedelta(1)
    context['x_axis'].reverse()

    print(context)
    return render(request, 'county_data.html', context)


def search(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
    else:
        search_text = ''

    counties = set()
    county_queries = set()

    if len(search_text) > 2:
        try:
            zip_code = int(search_text)
            zip_cities = City.objects.filter(zip_code__startswith=zip_code)
            for city in zip_cities:
                if len(counties) == 5:
                    break
                add_county(county_queries, city.county, "zip " + str(city.zip_code))
        except:
            counties = County.objects.filter(name__startswith=search_text)

    for county in counties:
        if len(counties) == 5:
            break
        add_county(county_queries, county, "county " + county.name)

    queries = list(county_queries)

    print(search_text)
    print(queries)

    return render(request, 'ajax_search.html', {'queries': queries})


def add_county(queries, county, note):
    if county not in queries:
        county.note = note
        county.state_initials = us_state_abbrev[county.state.name]
        queries.add(county)


def day_array_converter(arr, days):
    length = len(arr)
    ret = []
    sum = 0
    for i in range(0, length):
        if i/8 == days:
            break
        index = length - 1 - i
        sum += arr[index]
        if i % 8 == 7:
            ret.append(int(sum / 8.0))
    return ret

