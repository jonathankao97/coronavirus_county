from django.template.loader import render_to_string
from django.utils.html import strip_tags
from celery import task
from celery import shared_task
import os
# from scraper import sync_data as confirmed_sync
from test_case_scraper import sync_data as test_sync
from django.core.mail import send_mail
from coronavirus_county_stats.settings import EMAIL_HOST_USER
from county.models import Email, State, County
from county.views import us_state_abbrev


@shared_task(name="sync_data")
def sync_data(*args, **kwargs):
    confirmed_sync()


@shared_task(name="update_test_cases")
def update_test_cases(*args, **kwargs):
    test_sync()


@shared_task(name="send_feedback")
def send_feedback(data):
    email_content = "First Name: " + data['first_name'] + "\n" + "Last Name:" + data['last_name'] + "\n"
    email_content += "Email: " + data["email"] + "\n"
    email_content += "Feedback: " + data["feedback"] + "\n"
    send_mail("User Feedback", email_content, EMAIL_HOST_USER, [EMAIL_HOST_USER])


def helper(initial_list, add):
    initial_list.append(add)
    return initial_list


@shared_task(name="push_data")
def push_data(*args, **kwargs):
    for state in State.objects.all():
        state.set_confirmed(helper(state.get_confirmed(), state.today_delta_confirmed))
        state.set_deaths(helper(state.get_deaths(), state.today_delta_deaths))

    for county in County.objects.all():
        county.set_confirmed(helper(county.get_confirmed(), county.today_delta_confirmed))
        county.set_deaths(helper(county.get_deaths(), county.today_delta_deaths))


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



        html_message = render_to_string('email_template.html',
                                        {'county': email.county,
                                         'confirmed': confirmed_list[-1],
                                         'deaths': deaths_list[-1],
                                         'confirmed_change': confirmed_change,
                                         'deaths_change': deaths_change,
                                         'county_ranking': county_ranking_list[-1],
                                         'county_rank_sup': sups[min(4, county_ranking_list[-1])],
                                         'state_ranking': state_ranking_list[-1],
                                         'total_counties': len(County.objects.filter(state=email.county.state)),
                                         'positive': email.county.state.positive_tests,
                                         'negative': email.county.state.negative_tests,
                                         'state_rank_sup': sups[min(4, state_ranking_list[-1])],
                                         'county_ranking_change': county_ranking_change,
                                         'state_ranking_change': state_ranking_change,
                                         'state': email.county.state,
                                         'state_initials': us_state_abbrev[email.county.state.name],
                                         })
        plain_message = strip_tags(html_message)
        send_mail(email.county.name + " Clear Cov-19 Report", plain_message, EMAIL_HOST_USER,
                  [email.email], html_message=html_message)

