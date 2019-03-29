from rest_framework.permissions import BasePermission
from apps.items.models import Item
from constants import *


class ListAllRequestsPermission(BasePermission):

    def has_permission(self, request, view):

        return request.user.user_type != USER_CONSTANTS["BUYER"]


class ItemRequestPermission(BasePermission):
    
    def has_permission(self, request, view):
        
        return request.user.user_type != USER_CONSTANTS["SELLER"]


class RequestRetrievePermission(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        
        return not (request.user.user_type == USER_CONSTANTS["BUYER"] and obj.requester != request.user) 


class RequestDeletePermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        
        return request.user == obj.requester
