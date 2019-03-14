from __future__ import unicode_literals

from django.shortcuts import render

from rest_framework import mixins, viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from apps.users.serializers import UserSerializer, ChangePasswordSerializer
from apps.users.models import User


class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    API for signup , get user details and update user details
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [AllowAny, ]
        return super(UserViewSet, self).get_permissions()

    def get_object(self):
        return self.request.user

    def partial_update(self, request, **kwargs):
        print request.data
        # for k, v in request.META.items():
        #     print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        #     print k, '-------> ', v
        return super(UserViewSet, self).partial_update(request, **kwargs)


class ChangePassword(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    Api for Change Password
    """
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user


class Logout(APIView):
    """
    Api For Logout 
    """
    def delete(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

