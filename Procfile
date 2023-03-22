web: gunicorn events.wsgi --log-file -
worker: celery -A events worker --loglevel=info
beat: celery -A events beat -s /tmp/celerybeat-schedule
