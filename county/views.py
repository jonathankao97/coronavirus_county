from django.shortcuts import render

from county.models import City, County

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
    'Northern Mariana Islands':'MP',
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
    return render(request, 'county_data.html')


def search(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
    else:
        search_text = ''

    counties = set()
    cities = set()
    county_queries = set()
    city_queries = set()

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
            cities = City.objects.filter(name__startswith=search_text).order_by('city_size')

    for county in counties:
        if len(counties) == 5:
            break
        add_county(county_queries, county, "county " + county.name)

    for city in cities:
        if len(counties) == 5:
            break
        add_county(city_queries, city.county, "city " + city.name)

    queries = list(county_queries)
    for city_county in city_queries:
        if len(queries) == 5:
            break
        if city_county not in queries:
            queries.append(city_county)

    print(search_text)
    print(queries)

    return render(request, 'ajax_search.html', {'queries': queries})


def add_county(queries, county, note):
    if county not in queries:
        county.note = note
        county.state_initials = us_state_abbrev[county.state.name]
        queries.add(county)
