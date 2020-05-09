import os
import django
from django.db.models import Q

def clear_counties():
    for county in County.objects.all():
        county.set_confirmed([])
        county.set_deaths([])
        print(county.name, 'RESET')



def helper(initial_list, add):
    initial_list.append(add)
    return initial_list


def update_rest(count):
    for county in County.objects.all():
        if len(county.get_confirmed()) == 0:
            county.set_confirmed(helper(county.get_confirmed(), 0))
        elif len(county.get_confirmed()) != county:
            county.set_confirmed(helper(county.get_confirmed(), county.get_confirmed()[-1]))


def main():
    clear_counties()
    with open('nytimes.csv', 'r') as file:
        lines = file.readlines()
        date = '2020-01-21'
        count = 1
        # date, county, state, fips, cases, deaths
        for line in lines:
            stats = line.split(",")
            if stats[0] != date:
                date = stats[0]
                update_rest(count)
                print("NEXT DAY:", date)
                count += 1
            county = stats[1]
            state = stats[2]
            cases = int(stats[4])
            deaths = int(stats[5])

            c1 = Q(state__name=state)
            c2 = Q(name=county)
            q_set = County.objects.filter(c1 & c2)
            if q_set.count() == 0:
                print(county, 'NOT FOUND!')
            else:
                county_object = q_set[0]
                county_object.set_confirmed(helper(county_object.get_confirmed(), cases))
                county_object.set_deaths(helper(county_object.get_deaths(), deaths))
                print(county, 'UPDATED!')


if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coronavirus_county_stats.settings')
    django.setup()
    from county.models import County
    main()

