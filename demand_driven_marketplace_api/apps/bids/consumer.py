from channels import Group
from apps.bids.models import Bid
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Min


def ws_connect(message, pk):
    print message.content["path"]
    message.reply_channel.send({"accept": True, })
    Group("item-{}".format(pk)).add(message.reply_channel)