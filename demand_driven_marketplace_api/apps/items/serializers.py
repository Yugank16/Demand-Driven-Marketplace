from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from demand_driven_marketplace_api.settings import AUTH_USER_MODEL
from apps.items.models import Item
from apps.users.serializers import UserSerializer


class ItemListSerializer(serializers.ModelSerializer):
    """
    A Item Serializer provides fields for requests
    """
    requester = UserSerializer(read_only=True)

    class Meta(object):
        model = Item
        fields = ('id', 'name', 'max_price', 'requester', 'date_time', 'item_status')


class ItemSerializer(serializers.ModelSerializer):
    """
    A Item Serializer provides fields for requests
    """
    requester = UserSerializer()

    class Meta(object):
        model = Item
        fields = ('id',
                  'name',
                  'short_desc',
                  'requester',
                  'date_time',
                  'item_state',
                  'months_old',
                  'quantity_required',
                  'max_price',
                  'more_info',
                  'item_status'
                  )


