from django.core.management.base import BaseCommand
from county.models import State, County


class Command(BaseCommand):
    def handle(self, *args, **options):
        for state in State.objects.all():
            state.set_confirmed(state.get_confirmed()[1:])
            state.set_deaths(state.get_deaths()[1:])
            state.set_state_ranking(state.get_state_ranking()[1:])
            print("State", state.name, "updated!")

        for county in County.objects.all():
            county.set_confirmed(county.get_confirmed()[1:])
            county.set_deaths(county.get_deaths()[1:])
            county.set_state_county_ranking(county.get_state_county_ranking()[1:])
            print("County", county.name, "updated!")