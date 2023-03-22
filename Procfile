web: gunicorn events.wsgi --log-file -
worker: celery -A events worker -B --loglevel=info
