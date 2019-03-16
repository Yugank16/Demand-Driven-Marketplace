from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from rest_framework import viewsets, mixins, status
from rest_framework import filters

from apps.items.models import Item
from apps.items.serializers import ItemListSerializer, ItemSerializer


class ItemViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    ItemViewset Provides List Of All Item Request 
    """
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('item_status',)
    search_fields = ('name',)
    ordering_fields = ('max_price', 'date_time')

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.action == 'retrieve':
            return ItemSerializer
        elif self.action == 'list':
            return ItemListSerializer
    
    def get_queryset(self):
        if self.action == 'list':
            return Item.objects.exclude(requester=self.request.user).exclude(Q(item_status=3) | Q(item_status=4))
        return Item.objects.all()
    
    def get_serializer_context(self):
        return {'user': self.request.user}


