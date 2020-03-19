web: gunicorn coronavirus_county_stats.wsgi
celery_beat: celery -A coronavirus_county_stats beat -l info
worker: celery -A coronavirus_county_stats worker -l info
