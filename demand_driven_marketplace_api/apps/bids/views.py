from rest_framework import viewsets, mixins, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.bids.models import Bid
from apps.bids.serializers import BidSerializer, SpecificBidSerializer
from apps.commons.custom_permissions import *


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
                     viewsets.GenericViewSet):
    """
    ItemRequestBid To Create New Bid For An Item Request And List All Bid For An Item
    """
    serializer_class = BidSerializer

    def get_queryset(self):
        if self.action == 'list':
            return Bid.objects.filter(item__id=self.kwargs["item_pk"])
        return Bid.objects.all()


    def get_serializer_context(self):
        return {'user': self.request.user, 'item_pk': self.kwargs["item_pk"]}
            
    def get_permissions(self):     
        
        if self.action == 'list':
            self.permission_classes = [ListBidPermission, ]
        elif self.action == 'create':
            self.permission_classes = [BidPermission, ]
        return super(ItemRequestBid, self).get_permissions()
