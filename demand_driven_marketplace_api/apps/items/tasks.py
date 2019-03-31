from django.conf import settings

from celery import shared_task, task
from celery.schedules import crontab
from datetime import date, datetime, timedelta

from apps.commons.constants import *
from apps.items.models import Item


@task()
def change_item_status():
    one_hour_from_now = datetime.now() + timedelta(hours=1)
    items = Item.objects.filter(date_time__date=date.today(), date_time__hour=one_hour_from_now.hour, date_time__minute=one_hour_from_now.minute)
    for item in items:
        item.item_status = ITEM_CONSTANTS['ACTIVE']
        item.save()
    items = Item.objects.filter(date_time__date=date.today(), date_time__hour=datetime.now().hour, date_time__minute=datetime.now().minute)
    for item in items:
        item.item_status = ITEM_CONSTANTS['ONHOLD']
        item.save()    

