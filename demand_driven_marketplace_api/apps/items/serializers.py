from rest_framework import serializers
from rest_framework.exceptions import ValidationError

import datetime

from demand_driven_marketplace_api.settings import AUTH_USER_MODEL
from apps.items.models import Item
from apps.users.serializers import UserSerializer


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
        fields = ('id', 'name', 'short_description', 'requester', 'date_time', 'item_state', 'months_old',
                  'quantity_required', 'max_price', 'more_info', 'item_status')

    def create(self, validated_data):
        user = self.context['user']
        validated_data["requester"] = user
        print datetime.datetime.now()
        instance = super(ItemSerializer, self).create(validated_data)
        return instance


