from django.db import transaction

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.bids.models import Bid, ItemImage
from apps.items.models import Item
from apps.commons.constants import *


class ItemImageSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = ItemImage
        fields = ('image',)


class BidSerializer(serializers.ModelSerializer):
    """
    A Item List Serializer To List All Requests
    """
    images = serializers.ListField(child=serializers.ImageField(), write_only=True)

    class Meta(object):
        model = Bid
        fields = ('id', 'bid_price', 'description', 'validity', 'images') 

    def create(self, validated_data):
        item = self.context['item']
        user = self.context['user']
        try:
            item = Item.objects.get(pk=item)
        except Item.DoesNotExist:
            item = None
        if(not item):
            raise serializers.ValidationError("Item does not exist")

        validated_data["validity"] = BIDS_CONSTANTS["VALID"]
        validated_data["item"] = item
        validated_data["seller"] = user

        images = validated_data.pop("images")
        response = Bid.objects.filter(item__id=item.id, seller__id=user.id)
        
        if(len(response)):
            raise serializers.ValidationError("Only One Bid Allowed Per Item Request")

        if validated_data["item"].max_price < validated_data["bid_price"]:
            raise serializers.ValidationError("Bid price can not be greater than Max price")

        if validated_data["item"].item_status != ITEM_CONSTANTS["PENDING"]:
            raise serializers.ValidationError("Can not bid at this time")

        if len(images) != BIDS_CONSTANTS["IMAGE"]:
            raise serializers.ValidationError("Upload exactly {} images".format(BIDS_CONSTANTS["IMAGE"]))
         
        with transaction.atomic():
            instance = super(BidSerializer, self).create(validated_data)
            item_images = []
            for x in images:
                item_images.append(ItemImage(bid_id=instance.id, image=x))
            ItemImage.objects.bulk_create(item_images)
        return instance

    def update(self, instance, validated_data):
        
        if(len(validated_data) != 1 or not instance.validity == BIDS_CONSTANTS["VALID"] or not validated_data["validity"] or validated_data["validity"] != BIDS_CONSTANTS["INVALID"]):
            raise serializers.ValidationError("Can not Update the required field")
        return super(BidSerializer, self).update(instance, validated_data)


class SpecificBidSerializer(serializers.ModelSerializer):
    """
    Serializer to get particular bid details
    """
    images = ItemImageSerializer(source='itemimage', many=True, read_only=True)
    
    class Meta(object):
        model = Bid
        fields = '__all__'
    