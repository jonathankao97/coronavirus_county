from django.db import models
import json
# Create your models here.


class Feedback(models.Model):
    email = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    feedback = models.TextField()


class Email(models.Model):
    email = models.CharField(max_length=100)
    county = models.ForeignKey('County', on_delete=models.CASCADE)
    is_subscribed = models.BooleanField()

    def unsubscribe(self):
        self.is_subscribed = False
        self.save()

    def __str__(self):
        return self.email


class City(models.Model):
    zip_code = models.IntegerField(db_index=True)
    name = models.CharField(max_length=100, default="")
    # city_size = models.IntegerField()
    county = models.ForeignKey('County', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


def add_city(zip_code, name, county):
    print("GET OR CREATE", name)
    try:
        return City.objects.get_or_create(zip_code=zip_code, name=name, county=county)[0]
    except:
        print("BROKEN", name, zip_code, county)
        return City.objects.get_or_create(zip_code=zip_code, name=name, county=county)[0]


class County(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    fips_code = models.IntegerField()
    confirmed = models.CharField(default="[]", max_length=3600)
    deaths = models.CharField(default="[]", max_length=3600)
    state_county_ranking = models.CharField(default="[]", max_length=3600)
    state = models.ForeignKey('State', on_delete=models.CASCADE)
    recovered = models.IntegerField(default=0)

    today_delta_confirmed = models.IntegerField(default=0)
    today_delta_deaths = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def set_confirmed(self, x):
        County.objects.filter(id=self.id).update(confirmed=json.dumps(x))

    def get_confirmed(self):
        return json.loads(County.objects.filter(id=self.id)[0].confirmed)

    def set_deaths(self, x):
        County.objects.filter(id=self.id).update(deaths=json.dumps(x))

    def get_deaths(self):
        return json.loads(County.objects.filter(id=self.id)[0].deaths)

    def set_state_county_ranking(self, x):
        County.objects.filter(id=self.id).update(state_county_ranking=json.dumps(x))

    def get_state_county_ranking(self):
        return json.loads(County.objects.filter(id=self.id)[0].state_county_ranking)


def add_county(state, name, fips_code, confirmed, deaths, county_ranking, recovered):
    def helper(initial_list, add):
        initial_list.append(add)
        return initial_list

    if County.objects.filter(name=name, fips_code=fips_code).count() == 0:
        county_object = County(name=name, fips_code=fips_code)
        county_object.state = state
        county_object.save()
    else:
        county_object = County.objects.filter(name=name, fips_code=fips_code)[0]

    county_object.today_delta_confirmed = confirmed
    county_object.today_delta_deaths = deaths
    county_object.recovered = recovered
    county_object.set_state_county_ranking(helper(county_object.get_state_county_ranking(), county_ranking))
    county_object.save()
    return county_object


class State(models.Model):
    name = models.CharField(default="", max_length=100)
    confirmed = models.CharField(default="[]", max_length=3600)
    deaths = models.CharField(default="[]", max_length=3600)
    state_ranking = models.CharField(default="[]", max_length=3600)
    cumulative_hospitalized = models.CharField(default="[]", max_length=3600)
    past_positive_tests = models.CharField(default="[]", max_length=3600)
    past_negative_tests = models.CharField(default="[]", max_length=3600)

    positive_tests = models.IntegerField(default=0, blank=True)
    negative_tests = models.IntegerField(default=0, blank=True)
    today_hospitalized = models.IntegerField(default=0)

    today_delta_confirmed = models.IntegerField(default=0)
    today_delta_deaths = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def set_confirmed(self, x):
        State.objects.filter(id=self.id).update(confirmed=json.dumps(x))

    def get_confirmed(self):
        return json.loads(State.objects.filter(id=self.id)[0].confirmed)

    def set_deaths(self, x):
        State.objects.filter(id=self.id).update(deaths=json.dumps(x))

    def get_deaths(self):
        return json.loads(State.objects.filter(id=self.id)[0].deaths)

    def set_state_ranking(self, x):
        State.objects.filter(id=self.id).update(state_ranking=json.dumps(x))

    def get_state_ranking(self):
        return json.loads(State.objects.filter(id=self.id)[0].state_ranking)

    def set_hospitalized(self, x):
        State.objects.filter(id=self.id).update(cumulative_hospitalized=json.dumps(x))

    def get_hospitalized(self):
        return json.loads(State.objects.filter(id=self.id)[0].cumulative_hospitalized)

    def set_past_positive(self, x):
        State.objects.filter(id=self.id).update(past_positive_tests=json.dumps(x))

    def get_past_positive(self):
        return json.loads(State.objects.filter(id=self.id)[0].past_positive_tests)        

    def set_past_negative(self, x):
        State.objects.filter(id=self.id).update(past_negative_tests=json.dumps(x))

    def get_past_negative(self):
        return json.loads(State.objects.filter(id=self.id)[0].past_negative_tests)

    def set_positive_negative_hospitalized(self, positive_tests, negative_tests, today_hospitalized):
        State.objects.filter(id=self.id).update(positive_tests=positive_tests)
        State.objects.filter(id=self.id).update(negative_tests=negative_tests)
        State.objects.filter(id=self.id).update(today_hospitalized=today_hospitalized)


def add_state(name, confirmed, deaths, state_ranking):

    def helper(initial_list, add):
        initial_list.append(add)
        return initial_list

    if State.objects.filter(name=name).count() == 0:
        state_object = State(name=name)
        state_object.save()
    else:
        state_object = State.objects.filter(name=name)[0]
    state_object.today_delta_confirmed = confirmed
    state_object.today_delta_deaths = deaths
    state_object.set_state_ranking(helper(state_object.get_state_ranking(), state_ranking))
    state_object.save()
    return state_object
