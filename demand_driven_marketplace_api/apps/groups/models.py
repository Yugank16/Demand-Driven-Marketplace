from __future__ import unicode_literals

from django.db import models

from demand_driven_marketplace_api.constants import GLOBAL_CONSTANTS
from apps.users.models import User


class Group(models.Model):
    """
    Group Model For Storing Group Details
    """
    name = models.CharField(max_length=GLOBAL_CONSTANTS["TEXT_SIZE_SMALL"])
    group_info = models.CharField(max_length=GLOBAL_CONSTANTS["TEXT_SIZE_MEDIUM"])


class GroupMember(models.Model):
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    MEMBER_TYPE_CHOICES = (
        (1, 'Owner'),
        (2, 'Admin'),
        (3, 'Normal'),
    )
    member_type = models.PositiveSmallIntegerField(choices=MEMBER_TYPE_CHOICES)

