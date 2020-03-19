web: gunicorn coronavirus_county_stats.wsgi
worker: celery -A league_cast_project worker -l info
celery_beat: celery -A league_cast_project beat -l info