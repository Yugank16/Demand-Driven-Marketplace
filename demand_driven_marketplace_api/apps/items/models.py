from __future__ import unicode_literals

from django.db import models

from apps.commons.constants import GLOBAL_CONSTANTS
from django.conf import settings


class Item(models.Model):
    """
    Item Model For Storing Item Details Of Requester 
    """
    name = models.CharField(max_length=GLOBAL_CONSTANTS["TEXT_SIZE_SMALL"])
    short_description = models.CharField(max_length=GLOBAL_CONSTANTS["TEXT_SIZE_MEDIUM"])
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='items')
    date_time = models.DateTimeField()

    ITEM_STATE_CHOICES = (
        (1, 'New'),
        (2, 'Second Hand'),
        (3, 'Old'),
    )
    item_state = models.PositiveSmallIntegerField(choices=ITEM_STATE_CHOICES)

    months_old = models.PositiveSmallIntegerField()
    quantity_required = models.PositiveSmallIntegerField(default=1)
    max_price = models.PositiveIntegerField()
    more_info = models.CharField(max_length=GLOBAL_CONSTANTS["TEXT_SIZE_MEDIUM"], blank=True)
    
    ITEM_STATUS_CHOICES = (
        (1, 'pending'),
        (2, 'active'),
        (3, 'sold'),
        (4, 'unsold'),
    )
    item_status = models.PositiveSmallIntegerField(choices=ITEM_STATUS_CHOICES, default=1)



