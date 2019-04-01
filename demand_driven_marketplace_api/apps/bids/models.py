from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import JSONField

from apps.items.models import Item
from apps.commons.constants import GLOBAL_CONSTANTS


class Bid(models.Model):
    """
    Bid model that store the details of responses on Item Request
    """
    VALID = 1
    INVALID = 2
    SOLD = 3
    UNSOLD = 4
    PENDING = 5
    VALIDITY_CHOICES = (
        (VALID, 'Valid'),
        (INVALID, 'Invalid'),
        (SOLD, 'Sold'),
        (UNSOLD, 'Unsold'),
        (PENDING,'Pending'),
    )
    bid_price = models.PositiveIntegerField()
    item = models.ForeignKey(Item, related_name='bids')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='bids')
    description = models.CharField(max_length=GLOBAL_CONSTANTS["TEXT_SIZE_LARGE"])
    validity = models.PositiveSmallIntegerField(choices=VALIDITY_CHOICES, default=PENDING)
    payment_token = models.CharField(max_length=GLOBAL_CONSTANTS["TEXT_SIZE_MEDIUM"], blank=True, default="" ) 
    charge_info = JSONField(blank= True, null=True)

    def __str__(self):
        return '{}'.format(self.id)


class ItemImage(models.Model):
    """
    ItemImage model to save 
    """
    image = models.ImageField(upload_to='bid_item_photo/', null=True)
    bid = models.ForeignKey(Bid, related_name='item_images')

    def __str__(self):
        return '{}'.format(self.id)
   
