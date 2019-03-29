from django.conf import settings

from rest_framework import viewsets, mixins, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
import stripe

from apps.bids.models import Bid
from apps.bids.serializers import BidSerializer, SpecificBidSerializer, UpdateBidPaymentSerializer
from apps.commons.custom_permissions import *
from apps.commons.constants import *


class BidViewSet(mixins.ListModelMixin,
                 mixins.DestroyModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 viewsets.GenericViewSet):
    """
    BidViewSet To View Particular Bid details, Update Bid Validity,
    Delete Bid And List All Bids Made By User
    """
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SpecificBidSerializer
        return BidSerializer
    
    def get_queryset(self):
        if self.action == 'list':
            return Bid.objects.filter(seller=self.request.user)
        return Bid.objects.all()
    
    def get_permissions(self):

        if self.action == 'retrieve':
            self.permission_classes = [BidRetrievePermission, ]     
        elif self.action == 'destroy':
            self.permission_classes = [BidDeletePermission, ]
        elif self.action == 'partial_update':
            self.permission_classes = [BidUpdatePermission, ]
        return super(BidViewSet, self).get_permissions()


class ItemRequestBid(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    """
    ItemRequestBid To Create New Bid For An Item Request And List All Bid For An Item
    """

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
        token = serializer.data['payment_token']
        response_data = serializer.data
        try:
            charge = stripe.Charge.create(
                amount=100,
                currency='usd',
                description='Bidding Charge',
                source=token,
            )
            serializer.instance.charge_info = charge
            serializer.instance.validity = BIDS_CONSTANTS['VALID']
            serializer.instance.save()

            response_data['charge_info'] = charge
            response_data['validity'] = BIDS_CONSTANTS['VALID']
            
        except:
            pass    
        
        headers = self.get_success_headers(response_data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data= request.data
        if instance.validity== BIDS_CONSTANTS['PENDING'] and 'payment_token' in data:
            try:
                stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
                charge = stripe.Charge.create(
                    amount=GLOBAL_CONSTANTS['ONE_DOLLAR'],
                    currency='usd',
                    description='Bidding Charge',
                    source=data['payment_token'],
                )
                data['charge_info'] = charge
                data['validity'] = BIDS_CONSTANTS['VALID']
            except:
                pass
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def get_queryset(self):
        if self.action == 'list':
            return Bid.objects.filter(item__id=self.kwargs['item_pk'])
        return Bid.objects.all()

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return UpdateBidPaymentSerializer
        return BidSerializer
    def get_serializer_context(self):
        return {'user': self.request.user, 'item_pk': self.kwargs['item_pk']}
            
    def get_permissions(self):     
        
        if self.action == 'list':
            self.permission_classes = [ListBidPermission, ]
        elif self.action == 'create':
            self.permission_classes = [BidPermission, ]
        return super(ItemRequestBid, self).get_permissions()
