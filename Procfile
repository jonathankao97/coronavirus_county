web: gunicorn coronavirus_county_stats.wsgi
worker: celery -A coronavirus_county_stats worker -l info
celery_beat: celery -A coronavirus_county_stats -l info