import os
import django


def main():
    for county in County.objects.all():
        if len(county.get_confirmed()) != 0:
            county.today_delta_confirmed = county.get_confirmed()[-1]
            county.today_delta_deaths = county.get_deaths()[-1]
            print(county.name, 'updated')
            county.save()



if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coronavirus_county_stats.settings')
    django.setup()
    from county.models import County
    main()