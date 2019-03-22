from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from django_filters import rest_framework as filters
from rest_framework import viewsets, mixins, status
from rest_framework import filters as filter

from apps.items.models import Item
from apps.items.serializers import ItemListSerializer, ItemSerializer



class ItemFilter(filters.FilterSet):
    """
    Item Filter for searching item based on name
    """
    name = filters.CharFilter(name='name', lookup_expr='icontains')

    class Meta(object):
        model = Item
        fields = ['name', ]


class ItemViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    ItemViewset Provides List Of All Item Request 
    """
    filter_backends = (filters.DjangoFilterBackend, filter.OrderingFilter)
    filter_class = ItemFilter
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


