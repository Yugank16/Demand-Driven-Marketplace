from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings

from django.db.models import Q
from django_filters import rest_framework as filters

from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters as filter
import stripe

from apps.items.models import Item
from apps.items.serializers import ItemListSerializer, ItemSerializer
from apps.commons.constants import *
from apps.items.permissions import *


class ItemFilter(filters.FilterSet):
    """
    Item Filter for searching item based on name
    """
    name = filters.CharFilter(name='name', lookup_expr='icontains')

    class Meta(object):
        model = Item
        fields = ['name', 'item_status']


class ItemViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    ItemViewset Provides List Of All Item Request Made By Other Users ,
    Allows To Post A New Item Request and Get Details Of Particular Item Request
    """
    filter_backends = (filters.DjangoFilterBackend, filter.OrderingFilter)
    filter_class = ItemFilter
    ordering_fields = ('max_price', 'date_time')
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
        token = serializer.data['payment_token']
        response_data = serializer.data
        try:
            charge = stripe.Charge.create(
                amount=serializer.data['payment_amount'],
                currency='usd',
                description='Posting Item Request Charge',
                source=token,
            )
            serializer.instance.charge_info = charge
            serializer.instance.item_status = ITEM_CONSTANTS['PENDING']
            serializer.instance.save()
            
            response_data['charge_info'] = charge
            response_data['item_status'] = ITEM_CONSTANTS['PENDING']
            
        except:
            pass    
        
        headers = self.get_success_headers(response_data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)    
            
 
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data= request.data
        if instance.item_status== ITEM_CONSTANTS['PAYMENT_PENDING'] and 'payment_token' in data:
            try:
                stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
                charge = stripe.Charge.create(
                    amount=instance.payment_amount *GLOBAL_CONSTANTS[ONE_DOLLAR],
                    currency='usd',
                    description='Posting Item Request Charge',
                    source=data['payment_token'],
                )
                data['charge_info'] = charge
                data['item_status'] = ITEM_CONSTANTS['PENDING']
            except:
                pass
            
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
    
    
    def get_serializer_class(self):

        if self.action == 'list':
            return ItemListSerializer
        return ItemSerializer
        
    def get_queryset(self):
        if self.action == 'list':
            return Item.objects.exclude(requester=self.request.user).exclude(item_status__in=[ITEM_CONSTANTS['ONHOLD'],ITEM_CONSTANTS['SOLD'], ITEM_CONSTANTS['UNSOLD'],ITEM_CONSTANTS['PAYMENT_PENDING']])
        return Item.objects.all()
    
    def get_serializer_context(self):
        return {'user': self.request.user}
    
    def get_permissions(self):

        if self.action == 'retrieve':
            self.permission_classes = [RequestRetrievePermission, IsAuthenticated]  
        elif self.action == 'list':
            self.permission_classes = [ListAllRequestsPermission, IsAuthenticated]
        elif self.request.method == 'POST':
            self.permission_classes = [ItemRequestPermission, IsAuthenticated]

        return super(ItemViewSet, self).get_permissions()


class SelfItemRequest(mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    SelfItemRequest Provides List of Item Request Made by The User ,Allows To Delete the Request
    """

    filter_backends = (filters.DjangoFilterBackend, filter.OrderingFilter)
    filter_class = ItemFilter
    ordering_fields = ('max_price', 'date_time')

    def get_serializer_class(self):
        if self.action == 'list':
            return ItemListSerializer
        return ItemSerializer
    
    def get_queryset(self):
        if self.action == 'list':
            return Item.objects.filter(requester=self.request.user)
        return Item.objects.all()
    
    def get_permissions(self):

        if self.action == 'list':
            self.permission_classes = [ItemRequestPermission, IsAuthenticated]  
        elif self.action == 'destroy':
            self.permission_classes = [RequestDeleteUpdatePermission, IsAuthenticated]
        elif self.action == 'partial_update':
            self.permission_classes = [RequestDeleteUpdatePermission, IsAuthenticated]

        return super(SelfItemRequest, self).get_permissions()


