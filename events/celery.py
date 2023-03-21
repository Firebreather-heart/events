from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'events.settings')
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

app = Celery('events', broker='redis://127.0.0.1:6379/0')
app.config_from_object('django.conf:settings', namespace = 'CELERY')
#app.conf.broker_url = settings.BROKER_URL
app.autodiscover_tasks()
app.conf.CELERY_TRACK_STARTED = True
