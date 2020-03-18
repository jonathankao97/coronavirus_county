from django.db import models
import json
# Create your models here.


class City(models.Model):
    zip_code = models.IntegerField()
    name = models.CharField(max_length=100, default="")
    city_size = models.IntegerField()
    county = models.ForeignKey('County', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


def add_city(zip_code, name, city_size, county):
    return City.objects.get_or_create(zip_code=zip_code, name=name, city_size=city_size, county=county)[0]


class County(models.Model):
    name = models.CharField(max_length=100)
    fips_code = models.IntegerField()

    # TODO: turn into JSON Fields
    confirmed = models.CharField(default="[]", max_length=3600)
    confirmed_change = models.IntegerField()
    
    deaths = models.CharField(default="[]", max_length=3600)
    deaths_change = models.IntegerField()

    state_county_ranking = models.CharField(default="[]", max_length=3600)
    health_agency_data = models.CharField(default="", max_length=100)
    state = models.ForeignKey('State', on_delete=models.CASCADE)

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



def add_county(state, name, fips_code, confirmed, confirmed_change, deaths, deaths_change, county_ranking):
    def helper(initial_list, add):
        initial_list.append(add)
        return initial_list

    if County.objects.filter(name=name).count() == 0:
        county_object = County(name=name, fips_code=fips_code, confirmed_change=confirmed_change, deaths_change=deaths_change, state=state)
        county_object.save()
    else:
        county_object = County.objects.filter(name=name)[0]
        county_object.confirmed_change = confirmed_change
        county_object.deaths_change = deaths_change
        county_object.save()

    county_object.set_confirmed(helper(county_object.get_confirmed(), confirmed))
    county_object.set_deaths(helper(county_object.get_deaths(), deaths))
    county_object.set_state_county_ranking(helper(county_object.get_state_county_ranking(), county_ranking))
    return county_object


class State(models.Model):
    name = models.CharField(default="", max_length=100)

    # TODO: turn into JSON Fields
    confirmed = models.CharField(default="[]", max_length=3600)
    confirmed_change = models.IntegerField()
    deaths = models.CharField(default="[]", max_length=3600)
    deaths_change = models.IntegerField()
    state_ranking = models.CharField(default="[]", max_length=3600)

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


def add_state(name, confirmed, confirmed_change, deaths, deaths_change, state_ranking):

    def helper(initial_list, add):
        initial_list.append(add)
        return initial_list

    if State.objects.filter(name=name).count() == 0:
        state_object = State(name=name, confirmed_change=confirmed_change, deaths_change=deaths_change)
        state_object.save()
    else:
        state_object = State.objects.filter(name=name)[0]
        state_object.confirmed_change = confirmed_change
        state_object.deaths_change = deaths_change
        state_object.save()
    state_object.set_confirmed(helper(state_object.get_confirmed(), confirmed))
    state_object.set_deaths(helper(state_object.get_deaths(), deaths))
    state_object.set_state_ranking(helper(state_object.get_state_ranking(), state_ranking))
    return state_object







