from django.conf import settings

from rest_framework import viewsets, mixins, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
import stripe

from apps.bids.models import Bid
from apps.bids.serializers import BidSerializer, SpecificBidSerializer, UpdateBidPaymentSerializer, UpdateBidPriceSerializer, CheckBidForItemSerializer, MyBidsSerializer
from apps.commons.custom_permissions import *
from apps.commons.constants import *


class BidViewSet(mixins.ListModelMixin,
                 mixins.DestroyModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 viewsets.GenericViewSet):
    """
    BidViewSet To View Particular Bid details, Update Bid Validity(can be done only by item requester),
    Delete Bid And List All Bids Made By User
    """
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SpecificBidSerializer
        elif self.action == 'list':
            return MyBidsSerializer
        return BidSerializer
    
    def get_queryset(self):
        if self.action == 'list':
            return Bid.objects.filter(seller=self.request.user)
        return Bid.objects.all()
    
    def get_permissions(self):

        if self.action == 'retrieve':
            self.permission_classes = [BidRetrievePermission, IsAuthenticated]     
        elif self.action == 'destroy':
            self.permission_classes = [BidDeleteUpdatePermission, IsAuthenticated]
        elif self.action == 'partial_update':
            self.permission_classes = [BidUpdatePermission, IsAuthenticated]
        elif self.action == 'list':
            self.permission_classes = [MyBidsRetrievePermission, IsAuthenticated]
        return super(BidViewSet, self).get_permissions()


class ItemRequestBid(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    """
    ItemRequestBid To Create New Bid For An Item Request, List All Bid For An Item 
    And 
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
                amount=GLOBAL_CONSTANTS['ONE_DOLLAR'],
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
        if instance.validity== BIDS_CONSTANTS['PENDING'] and data.get('payment_token'):
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
            self.permission_classes = [ListBidPermission, IsAuthenticated]
        elif self.action == 'create':
            self.permission_classes = [BidPermission, IsAuthenticated]
        return super(ItemRequestBid, self).get_permissions()


class PriceUpdate(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    PriceUpdate For Seller To Update The Price Of Bid While Item Is Live
    """
    permission_classes = (IsAuthenticated, BidDeleteUpdatePermission)
    serializer_class = UpdateBidPriceSerializer
    queryset = Bid.objects.all()


class CheckBidForRequest(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    View to check bids for Item request by the logged in user
    """
    serializer_class = CheckBidForItemSerializer

    def get_queryset(self):
        return Bid.objects.filter(item__id=self.kwargs['item_pk'], seller=self.request.user)


class SoldBid(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    View to get details of sold bid against an item request
    """
    serializer_class = BidSerializer

    def get_queryset(self):
        return Bid.objects.filter(item__id=self.kwargs['item_pk'], validity=BIDS_CONSTANTS["SOLD"])
