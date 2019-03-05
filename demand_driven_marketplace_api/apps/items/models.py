from __future__ import unicode_literals

from django.db import models


from demand_driven_marketplace_api.constants import GLOBAL_CONSTANTS
from demand_driven_marketplace_api.settings import AUTH_USER_MODEL 


class Item(models.Model):
    """
    A class for requested items 
    
    * name of item
    * Short Desc
    * Requester
    * Date_time when required
    * State of item- new (1), second hand (2), old(3)
    * How many months old
    * visibility - (group id, null for public)
    * no. of items
    * max_price
    * other_info
    * status (pending(1) or completed(2) )
    """
    name = models.CharField(max_length=GLOBAL_CONSTANTS["TEXT_SIZE_SMALL"], blank=False)
    short_description = models.CharField(max_length=GLOBAL_CONSTANTS["TEXT_SIZE_MEDIUM"], blank=False)
    requester = models.ForeignKey(AUTH_USER_MODEL, related_name='items')
    date_time = models.DateTimeField(null=False, blank=False)

    ITEM_STATE_CHOICES = (
        (1, 'New'),
        (2, 'Second Hand'),
        (3, 'Old'),
    )
    item_state = models.PositiveSmallIntegerField(choices=ITEM_STATE_CHOICES)

    months_old = models.PositiveSmallIntegerField(blank=True)
    quantity_required = models.PositiveSmallIntegerField(default=1)
    max_price = models.PositiveIntegerField(blank=False, null=False)
    more_info = models.CharField(max_length=GLOBAL_CONSTANTS["TEXT_SIZE_MEDIUM"], blank=True)
    
    ITEM_STATUS_CHOICES = (
        (1, 'pending'),
        (2, 'active'),
        (3, 'sold'),
        (4, 'unsold'),
    )
    item_status = models.PositiveSmallIntegerField(choices=ITEM_STATUS_CHOICES)


