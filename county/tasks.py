from django.template.loader import render_to_string
from django.utils.html import strip_tags
from celery import task
from celery import shared_task
import os
# from scraper import sync_data as sync
from django.core.mail import send_mail
from coronavirus_county_stats.settings import EMAIL_HOST_USER
from county.models import Email

# #
# # We can have either registered task
# @shared_task(name="sync_data")
# def sync_data(*args, **kwargs):
#     print("hello")
#     sync()
#     # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coronavirus_county_stats.settings')
#


@shared_task(name="send_emails")
def send_emails(*args, **kwargs):
    for email in Email.objects.all():
        confirmed_list = email.county.get_confirmed()
        deaths_list = email.county.get_deaths()
        if len(confirmed_list) <= 1:
            confirmed_change = confirmed_list[0]
        else:
            confirmed_change = confirmed_list[-1] - confirmed_list[-2]

        if len(deaths_list) <= 1:
            deaths_change = deaths_list[0]
        else:
            deaths_change = deaths_list[-1] - deaths_list[-2]

        html_message = render_to_string('material-design-email-template/material-design-email-template/material-design.html',
                                        {'county': email.county,
                                         'confirmed': confirmed_list[-1],
                                         'deaths': deaths_list[-1],
                                         'confirmed_change': confirmed_change,
                                         'deaths_change': deaths_change})
        plain_message = strip_tags(html_message)
        send_mail("hello world", plain_message, EMAIL_HOST_USER,
                  [email.email], html_message=html_message)

