from django.db import models
import json
# Create your models here.


class City(models.Model):
    zip_code = models.IntegerField()
    name = models.CharField(max_length=100, default="")
    city_size = models.IntegerField()
    county = models.ForeignKey('County', on_delete=models.CASCADE)


def add_city(zip_code, name, city_size, county):
    return City.objects.get_or_create(zip_code=zip_code, name=name, city_size=city_size, county=county)[0]


class County(models.Model):
    name = models.CharField(default="", max_length=100)
    fips_code = models.IntegerField()

    # TODO: turn into JSON Fields
    confirmed = models.CharField(default="[]", max_length=3600)
    confirmed_change = models.CharField(default="[]", max_length=3600)
    deaths = models.CharField(default="[]", max_length=3600)
    deaths_change = models.CharField(default="[]", max_length=3600)

    county_ranking = models.IntegerField()
    health_agency_data = models.CharField(default="", max_length=100)
    state = models.ForeignKey('State', on_delete=models.CASCADE)

    def set_confirmed(self, x):
        print("confirmed updated!")
        County.objects.filter(id=self.id).update(confirmed=json.dumps(x))

    def get_confirmed(self):
        return json.loads(County.objects.filter(id=self.id)[0].confirmed)

    def set_confirmed_change(self, x):
        print("confirmed_changes updated!")
        County.objects.filter(id=self.id).update(confirmed_change=json.dumps(x))

    def get_confirmed_change(self):
        return json.loads(County.objects.filter(id=self.id)[0].confirmed_change)

    def set_deaths(self, x):
        print("deaths updated!")
        County.objects.filter(id=self.id).update(deaths=json.dumps(x))

    def get_deaths(self):
        return json.loads(County.objects.filter(id=self.id)[0].deaths)

    def set_deaths_change(self, x):
        print("deaths_change updated!")
        County.objects.filter(id=self.id).update(deaths_change=json.dumps(x))

    def get_deaths_change(self):
        return json.loads(County.objects.filter(id=self.id)[0].deaths_change)


def add_county(name, fips_code, confirmed, confirmed_change, deaths, deaths_change, county_ranking,health_agency_data):
    return City.objects.get_or_create(name=name, fips_code=fips_code, confirmed=confirmed, confirmed_change=confirmed_change,
                                      deaths=deaths, deaths_change=deaths_change,
                                      county_ranking=county_ranking,
                                      health_agency_data=health_agency_data)[0]


class State(models.Model):
    name = models.CharField(default="", max_length=100)

    # TODO: turn into JSON Fields
    confirmed = models.CharField(default="[]", max_length=3600)
    confirmed_change = models.CharField(default="[]", max_length=3600)
    deaths = models.CharField(default="[]", max_length=3600)
    deaths_change = models.CharField(default="[]", max_length=3600)
    state_ranking = models.CharField(default="[]", max_length=3600)

    def __str__(self):
        return self.name

    def set_confirmed(self, x):
        print("confirmed_changes updated!")
        State.objects.filter(id=self.id).update(confirmed=json.dumps(x))


    def get_confirmed(self):
        return json.loads(State.objects.filter(id=self.id)[0].confirmed)

    def set_confirmed_change(self, x):
        print("confirmed_changes updated!")
        State.objects.filter(id=self.id).update(confirmed_change=json.dumps(x))

    def get_confirmed_change(self):
        return json.loads(State.objects.filter(id=self.id)[0].confirmed_change)

    def set_deaths(self, x):
        print("deaths updated!")
        State.objects.filter(id=self.id).update(deaths=json.dumps(x))

    def get_deaths(self):
        return json.loads(State.objects.filter(id=self.id)[0].deaths)

    def set_deaths_change(self, x):
        print("deaths_change updated!")
        State.objects.filter(id=self.id).update(deaths_change=json.dumps(x))

    def get_deaths_change(self):
        return json.loads(State.objects.filter(id=self.id)[0].deaths_change)

    def set_state_ranking(self, x):
        print("state ranking updated!")
        State.objects.filter(id=self.id).update(state_ranking=json.dumps(x))

    def get_state_ranking(self):
        return json.loads(State.objects.filter(id=self.id)[0].state_ranking)



# confirmed, confirmed change, deaths, deaths_change, must be appended to the json list
def add_state(name, confirmed, confirmed_change, deaths, deaths_change, state_ranking):

    def helper(initial_list, add):
        initial_list.append(add)
        return initial_list

    state_object = State.objects.get_or_create(name=name)[0]
    state_object.set_confirmed(helper(state_object.get_confirmed(), confirmed))

    # state_object.set_confirmed(state_object.get_confirmed().append(confirmed))
    # state_object.set_confirmed_change(state_object.get_confirmed_change().append(confirmed_change))
    # state_object.set_deaths(state_object.get_deaths().append(deaths))
    # state_object.set_deaths_change(state_object.get_deaths_change().append(deaths_change))
    # state_object.set_state_ranking(state_object.get_state_ranking().append(state_ranking))
    return state_object







