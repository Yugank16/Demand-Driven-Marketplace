from rest_framework import viewsets, mixins, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.bids.models import Bid
from apps.bids.serializers import BidSerializer, SpecificBidSerializer
from apps.commons.custom_permissions import *


class BidViewSet(ModelViewSet):
    """
    BidViewSet To Create A New Bid For An Item request ,Update Bid Validity,Delete Bid And List All Bids For A Item Request
    """
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SpecificBidSerializer
        return BidSerializer
    
    def get_queryset(self):
        if self.action == 'list':
            return Bid.objects.filter(item__id=self.kwargs["pk"])
        return Bid.objects.all()
    
    def get_serializer_context(self):
        return {'user': self.request.user, 'item': self.kwargs["pk"]}

    def get_permissions(self):

        if self.action == 'retrieve':
            self.permission_classes = [BidRetrievePermission, ]
        elif self.action == 'list':
            self.permission_classes = [ListBidPermission, ]
        elif self.action == 'destroy':
            self.permission_classes = [BidDeletePermission, ]
        elif self.action == 'partial_update':
            self.permission_classes = [BidUpdatePermission, ]
        elif self.action == 'create':
            self.permission_classes = [BidPermission, ]

        return super(BidViewSet, self).get_permissions()
