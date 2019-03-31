from django.conf import settings

from celery import shared_task, task
from celery.schedules import crontab
from datetime import date, datetime, timedelta

from apps.commons.constants import *
from apps.items.models import Item


@task()
def change_item_status():
    hour_from_now = datetime.now() + timedelta(hours=1)
    hour_min_from_now = hour_from_now + timedelta(minutes=1)
    items = Item.objects.filter(item_status=ITEM_CONSTANTS['PENDING'], date_time__gte=hour_from_now, date_time__lt=hour_min_from_now)
    items.update(item_status=ITEM_CONSTANTS['ACTIVE'])
    
    min_from_now = datetime.now() + timedelta(minutes=1)
    items = Item.objects.filter(item_status=ITEM_CONSTANTS['ACTIVE'], date_time__gte=datetime.now(), date_time__lt=min_from_now)
    items.update(item_status=ITEM_CONSTANTS['ONHOLD'])
