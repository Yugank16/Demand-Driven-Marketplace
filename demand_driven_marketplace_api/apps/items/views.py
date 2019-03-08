from django.shortcuts import render

from rest_framework import viewsets, mixins, status

from apps.items.models import Item
from apps.items.serializers import ItemListSerializer, ItemSerializer


class ItemViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    ItemViewset Provides List Of All Item Request 
    """

    queryset = Item.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.action == 'retrieve':
            return ItemSerializer
        elif self.action == 'list':
            return ItemListSerializer
    
    def get_serializer_context(self):
        return {'user': self.request.user}


