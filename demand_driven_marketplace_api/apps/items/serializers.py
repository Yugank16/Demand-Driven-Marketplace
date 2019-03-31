from datetime import datetime, timedelta
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


from demand_driven_marketplace_api.settings import AUTH_USER_MODEL
from apps.items.models import Item
from apps.bids.models import Bid
from apps.users.serializers import UserSerializer
from apps.commons.constants import *


class ItemListSerializer(serializers.ModelSerializer):
    """
    A Item List Serializer To List All Requests
    """
    requester = UserSerializer(read_only=True)

    class Meta(object):
        model = Item
        fields = ('id', 'name', 'max_price', 'requester', 'date_time', 'item_status')


class ItemSerializer(serializers.ModelSerializer):
    """
    A Item Serializer To Create New Request
    """
    requester = UserSerializer(read_only=True)

    class Meta(object):
        model = Item
        fields = ('id', 'name', 'short_description', 'requester', 'date_time', 'item_state', 'months_old', 'payment_token', 'min_bid_price',
                  'quantity_required', 'max_price', 'more_info', 'item_status', 'payment_amount', 'charge_info')
        read_only_fields = ('payment_amount',)
        
    def create(self, validated_data):
        user = self.context['user']
        validated_data["requester"] = user
        instance = super(ItemSerializer, self).create(validated_data)
        return instance

    def validate_date_time(self, value):
        if datetime(value.year, value.month, value.day, value.hour, value.minute, 0) - datetime.now() < timedelta(hours=24):
            raise serializers.ValidationError({"date_time": "Required date_time and current date_time should have a difference of atleast 24hrs"})
        return value

    def validate(self, data):
        if self.instance:
            if self.instance.item_status in [ITEM_CONSTANTS['SOLD'], ITEM_CONSTANTS['UNSOLD']]:
                raise ValidationError("Unable to change Status for this item.")
        else:        
            payment_amount = int(0.01 * data['max_price'])
            data['payment_amount'] = max(GLOBAL_CONSTANTS['ONE_DOLLAR'], payment_amount)
        return data    

    def update(self, instance, validated_data):   

        if instance.item_status == ITEM_CONSTANTS['ONHOLD']: 
            selected_bid = Bid.objects.filter(item__id=instance.id, validity=BIDS_CONSTANTS['VALID']).order_by('bid_price').first()  
            if not selected_bid:
                validated_data['item_status'] = ITEM_CONSTANTS['UNSOLD']
            else:
                validated_data['item_status'] = ITEM_CONSTANTS['SOLD']
                selected_bid.validity = BIDS_CONSTANTS['SOLD']
                selected_bid.save()

        instance = super(ItemSerializer, self).update(instance, validated_data)
        return instance 


class ItemUpdateSerializer(serializers.ModelSerializer):
    """
    ItemUpdateSerializer to update time and max_price of item
    """
    class Meta(object):
        model = Item
        fields = '__all__'

    def validate(self, data):
        if(self.instance.item_status != 1 or not data.get("max_price") or len(data) > 1):
            raise ValidationError("Can not update the required field")
        return data
    



