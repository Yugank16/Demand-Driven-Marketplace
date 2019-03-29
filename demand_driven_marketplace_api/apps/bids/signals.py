from channels import Group
from apps.bids.models import Bid
from apps.items.models import Item
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Min
from channels.asgi import get_channel_layer
import json

@receiver([post_save, post_delete], sender=Bid)
def updatebid(sender, instance, **kwargs):
    min_price = Bid.objects.filter(item=instance.item).aggregate(Min('bid_price'))  
    min_price = min_price["bid_price__min"]
    item = Item.objects.get(pk=instance.item.id)
    message = {
        "min_price": min_price,
    }
    Group("item-{}".format(instance.item.id)).send({"text": json.dumps(message)})
    channel_layer = get_channel_layer()
    ch_group_list = channel_layer.group_channels("item-{}".format(instance.item.id))
    print "hello", len(ch_group_list)
    item.min_bid_price = min_price
    item.save()
    