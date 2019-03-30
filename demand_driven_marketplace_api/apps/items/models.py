from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from apps.commons.constants import GLOBAL_CONSTANTS


class Item(models.Model):
    """
    Item Model For Storing Item Detail

    name- name of item
    short_description
    requester- user requesting for item
    date_time- when required
    item_state- whether new, old or second hand
    months_old- for old items
    quantity required
    max_price
    more_info
    item_status - pending, active, sold or unsold
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
        (3, 'onhold'),
        (4, 'sold'),
        (5, 'unsold'),
    )
    item_status = models.PositiveSmallIntegerField(choices=ITEM_STATUS_CHOICES, default=1)

    def __str__(self):
        return '{}'.format(self.name)

    def __unicode__(self):
        return '{}'.format(self.name)
