from django.conf import settings

from celery import shared_task, task
from celery.schedules import crontab

@shared_task
def activate_item_request(id):
    print id

