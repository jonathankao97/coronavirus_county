from celery import task
from celery import shared_task
import os
from scraper import sync_data as sync
from django.core.mail import send_mail
from coronavirus_county_stats.settings import EMAIL_HOST_USER
from county.models import Email

#
# We can have either registered task
@shared_task(name="sync_data")
def sync_data(*args, **kwargs):
    print("hello")
    sync()
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coronavirus_county_stats.settings')



@shared_task(name="send_emails")
def send_emails(*args, **kwargs):
    for email in Email.objects.all():
        send_mail("hello world", "hello world", EMAIL_HOST_USER,
                  [email.email])

