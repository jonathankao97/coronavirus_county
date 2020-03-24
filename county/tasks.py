from django.template.loader import render_to_string
from django.utils.html import strip_tags
from celery import task
from celery import shared_task
import os
from scraper import sync_data as confirmed_sync
from test_case_scraper import sync_data as test_sync
from django.core.mail import send_mail
from coronavirus_county_stats.settings import EMAIL_HOST_USER
from county.models import Email

# #
# # We can have either registered task
@shared_task(name="sync_data")
def sync_data(*args, **kwargs):
    confirmed_sync()
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coronavirus_county_stats.settings')

@shared_task(name="update_test_cases")
def update_test_cases(*args, **kwargs):
    test_sync()




@shared_task(name="send_emails")
def send_emails(*args, **kwargs):
    for email in Email.objects.all():
        confirmed_list = email.county.get_confirmed()
        deaths_list = email.county.get_deaths()
        sups = ["aux", "st", "nd", "rd", "th"]

        if len(confirmed_list) <= 1:
            confirmed_change = confirmed_list[0]
        else:
            confirmed_change = confirmed_list[-1] - confirmed_list[-2]

        if len(deaths_list) <= 1:
            deaths_change = deaths_list[0]
        else:
            deaths_change = deaths_list[-1] - deaths_list[-2]

        county_ranking_list = email.county.get_state_county_ranking()
        state_ranking_list = email.county.state.get_state_ranking()
        if len(county_ranking_list) <= 1:
            county_ranking_change = county_ranking_list[0]
        else:
            county_ranking_change = county_ranking_list[-1] - county_ranking_list[-2]

        if len(state_ranking_list) <= 1:
            state_ranking_change = state_ranking_list[0]
        else:
            state_ranking_change = state_ranking_list[-1] - state_ranking_list[-2]



        html_message = render_to_string('email.html',
                                        {'county': email.county,
                                         'confirmed': confirmed_list[-1],
                                         'deaths': deaths_list[-1],
                                         'confirmed_change': confirmed_change,
                                         'deaths_change': deaths_change,
                                         'county_ranking': county_ranking_list[-1],
                                         'county_rank_sup': sups[min(4, county_ranking_list[-1])],
                                         'state_ranking': state_ranking_list[-1],
                                         'state_rank_sup': sups[min(4, state_ranking_list[-1])],
                                         'county_ranking_change': county_ranking_change,
                                         'state_ranking_change': state_ranking_change,
                                         })
        plain_message = strip_tags(html_message)
        send_mail(email.county.name + " Clear Cov-19 Report", plain_message, EMAIL_HOST_USER,
                  [email.email], html_message=html_message)

