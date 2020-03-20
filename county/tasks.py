from celery import task
from celery import shared_task
import os
from scraper import sync_data as sync

# We can have either registered task
@shared_task(name="sync_data")
def sync_data(*args, **kwargs):
    print("hello")
    sync()
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coronavirus_county_stats.settings')

