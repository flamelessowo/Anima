from __future__ import absolute_import
import os
from celery import Celery


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Anima.settings')
app = Celery('Anima', backend='redis://localhost:6379/0', broker='pyamqp://')

app.config_from_object('django.conf.settings', namespace='CELERY')

app.autodiscover_tasks()
