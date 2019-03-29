from channels import Group
from apps.bids.models import Bid
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Min
import json

def ws_connect(message, pk):
    print "sadasdsadasd"
    print message.content["path"]
    message.reply_channel.send({"accept": True, })
    Group("item-{}".format(pk)).add(message.reply_channel)

@receiver([post_save, post_delete], sender=Bid)
def updatebid(sender, instance, **kwargs):
    print sender
    print instance.item
    min_price = Bid.objects.filter(item=instance.item).aggregate(Min('bid_price'))
    print instance.item.id,  
    min_price = min_price["bid_price__min"]
    message = {
        "min_price": min_price,
    }
    Group("item-{}".format(instance.item.id)).send({"text": json.dumps(message)})