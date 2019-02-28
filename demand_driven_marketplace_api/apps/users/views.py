from __future__ import unicode_literals

from django.shortcuts import render

from rest_framework import mixins, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.users.serializers import UserSerializer


class UserViewSet(mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    """
    API for signup
    """
    serializer_class = UserSerializer


class Logout(APIView):
    """
    Api For Logout 
    """
    def delete(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)