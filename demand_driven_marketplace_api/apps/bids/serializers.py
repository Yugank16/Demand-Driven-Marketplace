from django.db import transaction

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.bids.models import Bid, ItemImage
from apps.items.models import Item
from apps.items.serializers import ItemListSerializer
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
            if(len(data) > 1 or 3 <= self.instance.validity <= 4 or 3 <= data["validity"] <= 4):
                raise ValidationError("Can not update the required field")
        return data
        
    def create(self, validated_data):
        item_pk = self.context['item_pk']
        user = self.context['user']
        try:
            item = Item.objects.get(pk=item_pk)
        except Item.DoesNotExist:
            item = None
        if(not item):
            raise serializers.ValidationError("Item does not exist")

        validated_data["validity"] = BIDS_CONSTANTS['PENDING']
        validated_data["item"] = item
        validated_data["seller"] = user

        images = validated_data.pop("images")
        response = Bid.objects.filter(item__id=item.id, seller__id=user.id)
        
        if(len(response)):
            raise serializers.ValidationError("Only One Bid Allowed Per Item Request")

        if validated_data["item"].max_price < validated_data["bid_price"]:
            raise serializers.ValidationError({'bid_price': "Bid price can not be greater than Max price"})

        if validated_data["item"].item_status != ITEM_CONSTANTS["ACTIVE"]:
            raise serializers.ValidationError("Can not bid at this time")

        if len(images) < BIDS_CONSTANTS["IMAGE"]:
            raise serializers.ValidationError({'images': "Upload Atleast {} images".format(BIDS_CONSTANTS["IMAGE"])})
         
        with transaction.atomic():
            instance = super(BidSerializer, self).create(validated_data)
            item_images = []
            for x in images:
                item_images.append(ItemImage(bid_id=instance.id, image=x))
            ItemImage.objects.bulk_create(item_images)
        return instance


class SpecificBidSerializer(serializers.ModelSerializer):
    """
    Serializer to get particular bid details
    """
    images = ItemImageSerializer(source='item_image', many=True)
    seller = UserSerializer(read_only=True)
    item = ItemListSerializer(read_only=True)

    class Meta(object):
        model = Bid
        fields = '__all__'

class UpdateBidPaymentSerializer(serializers.ModelSerializer):
    """
    Serializer to retry payment for bidding
    """
    class Meta(object):
        model = Bid
        fields = ('id', 'validity', 'payment_token', 'charge_info')
    
    