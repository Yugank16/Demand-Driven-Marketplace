from rest_framework.permissions import BasePermission
from apps.items.models import Item
from apps.commons.constants import *


class ListAllRequestsPermission(BasePermission):
    """
    List of Item request is not for user type buyer
    """
    def has_permission(self, request, view):

        return request.user.user_type != USER_CONSTANTS["BUYER"]


class ItemRequestPermission(BasePermission):
    """
    User type seller is not allowed to Place Item request
    """
    def has_permission(self, request, view):
        
        return request.user.user_type != USER_CONSTANTS["SELLER"]


class RequestRetrievePermission(BasePermission):
    """
    Item Request details is not available if usertype is buyer and has not requested the item 
    """
    def has_object_permission(self, request, view, obj):
        
        return not (request.user.user_type == USER_CONSTANTS["BUYER"] and obj.requester != request.user) 


class RequestDeleteUpdatePermission(BasePermission):
    """
    Delete and update permission is only for the user who requested for the item
    """
    def has_object_permission(self, request, view, obj):
        
        return request.user == obj.requester and obj.item_status == ITEM_CONSTANTS["PENDING"]
