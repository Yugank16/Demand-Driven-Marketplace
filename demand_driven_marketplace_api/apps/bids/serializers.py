from django.db import transaction

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.bids.models import Bid, ItemImage
from apps.items.models import Item
from apps.items.serializers import ItemListSerializer, ItemBidSerializer
from apps.users.serializers import UserSerializer
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
    seller = UserSerializer(read_only=True)
    item = ItemListSerializer(read_only=True)

    class Meta(object):
        model = Bid
        fields = ('id', 'bid_price', 'description', 'seller', 'item', 'validity', 'images', 'payment_token', 'charge_info') 
    
    def validate(self, data):

        if(self.instance):
            if(len(data) > 1 or not data.get('validity') or 3 <= self.instance.validity <= 4 
            or BIDS_CONSTANTS['SOLD'] <= data["validity"] <= BIDS_CONSTANTS['UNSOLD']):
                raise ValidationError("Can not update the required field")
        else:
            item_pk = self.context['item_pk']
            user = self.context['user']
            try:
                item = Item.objects.get(pk=item_pk)
            except Item.DoesNotExist:
                item = None
            if(not item):
                raise ValidationError("Item does not exist")
            data["validity"] = BIDS_CONSTANTS["VALID"]
            data["item"] = item
            data["seller"] = user
            images = data["images"]
            response = Bid.objects.filter(item__id=item.id, seller__id=user.id)

            if(len(response)):
                raise ValidationError({'valid': "Only One Bid Allowed Per Item Request"})

            if data["item"].max_price < data["bid_price"]:
                raise ValidationError({'bid_price': "Bid price can not be greater than ask price by requester"})

            if data["item"].item_status != ITEM_CONSTANTS["ACTIVE"]:
                raise ValidationError({'time': "Can not bid at this time"})

            if len(images) < BIDS_CONSTANTS["IMAGE"]:
                raise ValidationError({'images': "Upload Atleast {} images".format(BIDS_CONSTANTS["IMAGE"])})

        return data
        
    def create(self, validated_data):  
        images = validated_data.pop("images")
        with transaction.atomic():
            instance = super(BidSerializer, self).create(validated_data)
            item_images = []
            for image in images:
                item_images.append(ItemImage(bid_id=instance.id, image=image))
            ItemImage.objects.bulk_create(item_images)
        return instance


class SpecificBidSerializer(serializers.ModelSerializer):
    """
    Serializer to get particular bid details
    """
    images = ItemImageSerializer(source='item_images', many=True)
    seller = UserSerializer(read_only=True)
    item = ItemListSerializer(read_only=True)

    class Meta(object):
        model = Bid
        fields = ('id', 'bid_price', 'description', 'seller', 'item', 'validity', 'images') 
    

class UpdateBidPriceSerializer(serializers.ModelSerializer):
    """
    Serializer To Update Bid Price
    """
    class Meta(object):
        model = Bid
        fields = '__all__' 

    def validate(self, data):
        if(len(data) > 1 or self.instance.item.item_status != 2 or not data.get('bid_price')):
            raise ValidationError("Can not update the required field")
        if(data["bid_price"] > self.instance.item.max_price):
            raise ValidationError({'bid_price': "Bid price can not be greater than ask price by requester"})
        return data


class UpdateBidPaymentSerializer(serializers.ModelSerializer):
    """
    Serializer to retry payment for bidding
    """
    class Meta(object):
        model = Bid
        fields = ('id', 'validity', 'payment_token', 'charge_info')


class CheckBidForItemSerializer(serializers.ModelSerializer):
    """
    Serializer to check bids for Item request
    """
    class Meta(object):
        model = Bid
        fields = ('id',)

            
class MyBidsSerializer(serializers.ModelSerializer):
    """
    Serializer to get list of self bids
    """
    item = ItemBidSerializer(read_only=True)

    class Meta(object):
        model = Bid
        fields = ('id', 'bid_price', 'item') 