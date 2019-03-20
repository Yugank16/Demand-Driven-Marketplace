from __future__ import unicode_literals

from django.contrib.auth.tokens import PasswordResetTokenGenerator, default_token_generator
from django.conf import settings
from django.shortcuts import render

from rest_framework import mixins, viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.serializers import UserSerializer, EmailSerializer, ChangePasswordSerializer, PasswordTokenSerializer
from apps.users.models import User
from apps.users.tasks import send_reset_email_task
from apps.commons.constants import *
from apps.commons.custom_permissions import *


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


class ResetPasswordRequestToken(GenericAPIView):
    """
    An Api View which provides a method to request a password reset token 
    based on an e-mail address
    """
    permission_classes = (AllowAnonymous,)
    serializer_class = EmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        user = User.objects.filter(email__iexact=email).first()
        active_user_found = False
        if user:
            active_user_found = True

        if not active_user_found:
            return Response({'data': MESSAGE_CONSTANTS["LINK_SENT_MESSAGE"], 'status': status.HTTP_200_OK})

        token = PasswordResetTokenGenerator.make_token(
            default_token_generator, user)

        reset_url = '{}{}/{}/{}/'.format(settings.LOCALHOST, MESSAGE_CONSTANTS["PASSWORD_RESET_CONFIRM_URL"], user.id, token)
        send_reset_email_task.delay(email, user.get_short_name(), reset_url)
        return Response({'data': MESSAGE_CONSTANTS["LINK_SENT_MESSAGE"], 'status': status.HTTP_200_OK})


class ResetPasswordTokenVerification(GenericAPIView):
    """
    An Api View which checks whether token is valid or not
    """
    permission_classes = (AllowAnonymous,)
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        token = self.kwargs.get('token')
        if not PasswordResetTokenGenerator.check_token(default_token_generator, user, token):
            return Response({'data': MESSAGE_CONSTANTS["INVALID_TOKEN"],
                             'status': status.HTTP_400_BAD_REQUEST})
        return Response({'status': status.HTTP_200_OK})


class ResetPasswordConfirm(GenericAPIView):
    """
    An Api View which provides a method to reset a password based on a unique
    token
    """
    permission_classes = (AllowAnonymous,)
    serializer_class = PasswordTokenSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data['password']

        token = self.kwargs.get('token')
        user = self.get_object()

        if not PasswordResetTokenGenerator.check_token(default_token_generator, user, token):
            return Response({'data': MESSAGE_CONSTANTS["INVALID_TOKEN"], 'status': status.HTTP_400_BAD_REQUEST})

        user.set_password(password)
        user.save()

        return Response({'data': MESSAGE_CONSTANTS["PASSWORD_SET"], 'status': status.HTTP_200_OK})
