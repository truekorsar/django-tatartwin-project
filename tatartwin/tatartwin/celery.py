from __future__ import absolute_import, unicode_literals

from celery import Celery
from . import celeryconfig
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tatartwin.settings')

app = Celery('tatartwin')

app.config_from_object(celeryconfig)

app.autodiscover_tasks()
