from django.shortcuts import render

from rest_framework import viewsets, mixins, status

from apps.items.models import Item
from apps.items.serializers import ItemListSerializer


class ItemViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet
):
    """
    ItemViewset provides `list()' of requests which contain
    name,
    max_price,
    requester,
    date_time
    """
    
    serializer_class = ItemListSerializer
    queryset = Item.objects.all()

    def get_serializer_context(self):
        return {'user': self.request.user}

