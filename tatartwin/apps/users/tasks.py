from __future__ import absolute_import, unicode_literals
from celery.task import periodic_task
from celery.schedules import crontab
from django.utils import timezone
from datetime import timedelta
from .models import TatarUser


@periodic_task(run_every=crontab(minute='*/1'), name='delete_inactive_users')
def delete_inactive_users():
    now = timezone.now()
    TatarUser.objects.filter(is_active=False, date_joined__lte=now-timedelta(minutes=30)).delete()



