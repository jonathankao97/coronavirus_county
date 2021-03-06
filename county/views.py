from django.shortcuts import render, redirect, HttpResponseRedirect
from county.models import City, County, State, Email
from django.utils import timezone
from datetime import timedelta
from county.forms import EmailSignUp
from math import log

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


def unsubscribe(request):
    form = EmailSignUp()
    if request.method == 'POST':
        form = EmailSignUp(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            for email in Email.objects.filter(email=email):
                email.unsubscribe()
            return redirect('test')
    context = {
        'form': form
    }
    return render(request, 'unsubscribe.html', context)


def mail_signup(request, county_id):
    county = County.objects.filter(id=county_id)[0]
    if request.method == 'POST':
        form = EmailSignUp(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            create_email = Email(email=email, county=county, is_subscribed=True)
            create_email.save()
            return redirect('data', county_id=county_id)
    else:
        form = EmailSignUp()

    context = {
        'form': form,
        'county': county,
    }
    return render(request, 'mail_signup.html', context)


def mail(request):
    return render(request, 'material-design-email-template/material-design-email-template/material-design.html')


def test(request):
    return render(request, 'test.html', context={'search_vis': 'd-none',
                                                 'is_home': True})


def hello(request):
    return render(request, 'hello.html')


def data(request, county_id):
    sups = ["aux", "st", "nd", "rd", "th"]
    county = County.objects.get(id=county_id)

    confirmed = county.get_confirmed()
    confirmed.append(county.today_delta_confirmed)
    print(confirmed)
    beg = max(0, len(confirmed) - 90)
    confirmed = confirmed[beg:]

    hospitalized_hist = county.state.get_hospitalized()
    hospitalized_hist.append(county.state.today_hospitalized)
    hospitalized_hist = hospitalized_hist[beg:]

    positive_hist = county.state.get_past_positive()
    positive_hist.append(county.state.positive_tests)
    positive_hist = positive_hist[beg:]

    negative_hist = county.state.get_past_negative()
    negative_hist.append(county.state.negative_tests)
    negative_hist = negative_hist[beg:]

    deltas = [1, 7, 30]
    confirmed_deltas = []
    deaths_deltas = []
    for i in range(0, len(deltas)):
        delta = deltas[i]
        if len(confirmed) > delta:
            confirmed_deltas.append(confirmed[-1] - confirmed[-(1 + delta)])
        else:
            confirmed_deltas.append("n/a")
    confirmed_increase = 0
    if len(confirmed) >= 2 and confirmed[-2] != 0:
        confirmed_increase = int(float(confirmed_deltas[0] * 100) / confirmed[-2])
    deaths = county.get_deaths()
    deaths.append(county.today_delta_deaths)
    beg = max(0, len(deaths) - 90)
    deaths = deaths[beg:]
    for i in range(0, len(deltas)):
        delta = deltas[i]
        if len(confirmed) > delta:
            deaths_deltas.append(deaths[-1] - deaths[-(1 + delta)])
        else:
            deaths_deltas.append("n/a")
    deaths_increase = 0
    if len(deaths) >= 2 and deaths[-2] != 0:
        deaths_increase = int(float(deaths_deltas[0] * 100) / deaths[-2])
    if len(county.get_state_county_ranking()) > 0:
        county_rank = int(county.get_state_county_ranking()[-1])
    else:
        county_rank = 'n/a'
    state_rank = int(county.state.get_state_ranking()[-1])

    context = {
        'confirmed': confirmed,
        'current_confirmed': county.today_delta_confirmed,
        'log_confirmed': log_arr(confirmed),
        'current_deaths': county.today_delta_deaths,
        'confirmed_deltas': confirmed_deltas,
        'confirmed_increase': confirmed_increase,
        'deaths': deaths,
        'log_deaths': log_arr(deaths),
        'deaths_deltas': deaths_deltas,
        'death_increase': deaths_increase,
        'county_rank': county_rank,
        'county_rank_sup': sups[min(4, county_rank)] if county_rank != 'n/a' else '',
        'state_rank': state_rank,
        'state_rank_sup': sups[min(4, state_rank)],
        'state_total_counties': len(County.objects.filter(state=county.state)),
        'state_initials': us_state_abbrev[county.state.name],
        'county': county,
        'positive': county.state.positive_tests,
        'negative': county.state.negative_tests,
        'state': county.state,
        'recovered': county.recovered,
        'positive_hist': positive_hist,
        'negative_hist': negative_hist,
        'hospitalized_hist': hospitalized_hist,
        'x_axis': [],
        'is_vis': 'd-none',
        'is_data': True,
        'hospital': 1,
    }
    if county.state.today_hospitalized == -1:
        context['hospitalized'] = "n/a"
        context['hospital'] = 0
    else:
        context['hospitalized'] = county.state.today_hospitalized

    if hospitalized_hist[-2] != 0:
        context['hospital_increase'] = int((hospitalized_hist[-1] - hospitalized_hist[-2]) * 100 / hospitalized_hist[-2])
    else:
        context['hospital_increase'] = 0
    now = timezone.localtime(timezone.now())
    for i in range(0, min(len(confirmed), 90)):
        context['x_axis'].append(now.strftime('%-m/%-d'))
        now -= timedelta(1)
    context['x_axis'].reverse()
    print(context)
    return render(request, 'county_data.html', context)


def log_arr(array):
    log_deaths = []
    for val in array:
        if val == 0:
            log_deaths.append(0)
        else:
            log_deaths.append(int(log(val, 2)))
    return log_deaths


def subscribe(request):
    county_id = request.POST['county_id']
    email = request.POST['email']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']

    county = County.objects.get(id=county_id)
    create_email = Email(email=email, county=county, is_subscribed=True)
    create_email.save()

    return render(request, 'aux.html')


def search1(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
    else:
        search_text = ''

    queries = set()

    if len(search_text) > 2:
        try:
            zip_code = int(search_text)
            zip_cities = City.objects.filter(zip_code__startswith=zip_code)
            for city in zip_cities:
                add_county(queries, city.county, "zip " + str(city.zip_code))
        except ValueError:
            counties = County.objects.filter(name__icontains=search_text)

            for county in counties:
                add_county(queries, county, "county " + county.name)

    print(search_text)
    print(list(queries))

    return render(request, 'ajax_search1.html', {'queries': list(queries)})


def feedback(request):
    print(request.POST)

    email = request.POST['email']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    feedback = request.POST['feedback']
    print("FEEDBACK RECEIVED", email, first_name, last_name, feedback)

    from county.models import Feedback
    sender_feedback = Feedback(email=email, first_name=first_name, last_name=last_name, feedback=feedback)
    sender_feedback.save()

    return render(request, 'base.html')


def search(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
    else:
        search_text = ''

    queries = set()

    if len(search_text) > 2:
        try:
            zip_code = int(search_text)
            zip_cities = City.objects.filter(zip_code__startswith=zip_code)
            for city in zip_cities:
                add_county(queries, city.county, "zip " + str(city.zip_code))
        except ValueError:
            counties = County.objects.filter(name__icontains=search_text)

            for county in counties:
                add_county(queries, county, "county " + county.name)

    print(search_text)
    print(list(queries))

    return render(request, 'ajax_search.html', {'queries': list(queries)})


def add_county(queries, county, note):
    if county not in queries:
        county.note = note
        county.state_initials = us_state_abbrev[county.state.name]
        queries.add(county)
