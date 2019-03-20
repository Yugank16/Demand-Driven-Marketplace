from __future__ import absolute_import, unicode_literals
import os

from django.conf import settings

from celery import Celery

exists = os.path.exists('demand_driven_marketplace_api/local_settings.py')
if exists:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demand_driven_marketplace_api.local_settings")
else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demand_driven_marketplace_api.settings")
    
app = Celery('demand_driven_marketplace_api')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()