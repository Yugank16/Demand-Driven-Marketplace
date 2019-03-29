from rest_framework.permissions import BasePermission
from apps.items.models import Item
from apps.bids.models import Bid
from apps.commons.constants import *


class AllowAnonymous(BasePermission):

    def has_permission(self, request, view):
        """
        Permission for anonymous users only
        """
        return bool(request.user and not request.user.is_authenticated)


class BidPermission(BasePermission):

    def has_permission(self, request, view):
        try:
            item = Item.objects.get(pk=view.kwargs["item_pk"])
        except Item.DoesNotExist:
            item = None
        if(not item):
            return False
        return request.user != item.requester and request.user.user_type != USER_CONSTANTS["BUYER"]
 

class BidDeletePermission(BasePermission):
    """
    Delete is allowed only for Seller who posted the bid
    """
    def has_object_permission(self, request, view, obj):
        
        return request.user == obj.seller


class BidRetrievePermission(BasePermission):
    """
    Item requester and Seller who posted the Bid are allowed to get details of particular bid
    """
    def has_object_permission(self, request, view, obj):
        
        return request.user == obj.seller or request.user == obj.item.requester


class ListBidPermission(BasePermission):
    """
    Item requester is allowed to get list of all the bids on his/her item request
    """
    def has_permission(self, request, view):
        
        try:
            item = Item.objects.get(pk=view.kwargs["item_pk"])
        except Item.DoesNotExist:
            item = None
        if(not item):
            return False
        return request.user == item.requester
    

class BidUpdatePermission(BasePermission):
    """
    Item requester is allowed to change the status of bid from valid to invalid
    """
    def has_object_permission(self, request, view, obj):
        
        return request.user == obj.item.requester


class BidPriceUpdatePermission(BasePermission):
    """
    Item requester is allowed to change the status of bid from valid to invalid
    """
    def has_object_permission(self, request, view, obj):
        
        return request.user == obj.seller
