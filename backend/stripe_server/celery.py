import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'stripe_server.settings')

app = Celery('stripe_server')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
