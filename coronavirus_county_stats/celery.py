# http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coronavirus_county_stats.settings')

app = Celery('coronavirus_county_stats')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


app.conf.beat_schedule = {

    'sync_data': {
        'task': 'sync_data',
        # 'schedule': 10800.0,
        'schedule': crontab(minute=0, hour='*/3'),
        'args': ()
    },

}