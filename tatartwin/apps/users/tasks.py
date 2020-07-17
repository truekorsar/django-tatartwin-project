from __future__ import absolute_import, unicode_literals
from celery.schedules import crontab
from .models import TatarUser
from tatartwin import celery_app


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=3, minute=0),
                             delete_inactive_users.s(), name='delete inactive users')


@celery_app.task
def delete_inactive_users():
    TatarUser.objects.filter(is_active=False).delete()



