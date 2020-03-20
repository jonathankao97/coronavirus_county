from django.shortcuts import render
from county.models import City, County
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


def test(request):

    return render(request, 'test.html')


def data(request, county_id):
    county = County.objects.get(id=county_id)
    confirmed = county.get_confirmed()
    confirmed_delta = confirmed[-1] - confirmed[-2]
    deaths = county.get_deaths()
    deaths_delta = deaths[-1] - deaths[-2]

    context = {
        'confirmed': confirmed,
        'confirmed_delta': confirmed_delta,
        'confirmed_increase': int(float(confirmed_delta * 100) / confirmed[-2]) if confirmed[-2] != 0 else 0,
        'deaths': deaths,
        'deaths_delta': deaths_delta,
        'death_increase': int(float(confirmed_delta * 100) / confirmed[-2]) if deaths[-2] != 0 else 0,
        'county_rank': county.state_county_ranking,
        'x_axis': [],
    }

    now = timezone.localtime(timezone.now())
    for i in range(0, min(len(confirmed), 14)):
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
