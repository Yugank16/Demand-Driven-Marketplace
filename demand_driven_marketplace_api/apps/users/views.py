from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import mixins, viewsets

from apps.users.serializers import UserSerializer


class UserViewSet(mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    """
    API for signup
    """
    serializer_class = UserSerializer
