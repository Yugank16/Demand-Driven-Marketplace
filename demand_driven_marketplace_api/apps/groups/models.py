from __future__ import unicode_literals

from django.db import models

from apps.users.models import User


class Group(models.Model):
    """
    Group Model For Storing Group Details
    """
    name = models.CharField(max_length=CONSTANTS["TEXT_SIZE_MEDIUM"])
    group_info = models.CharField(max_length=CONSTANTS["TEXT_SIZE_LARGE"])


class GroupMember(models.Model):
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    MEMBER_TYPE_CHOICES = (
        (1, 'Owner'),
        (2, 'Admin'),
        (3, 'Normal'),
    )
    member_type = models.PositiveSmallIntegerField(choices=MEMBER_TYPE_CHOICES)

