from __future__ import unicode_literals

from django.contrib.auth.tokens import PasswordResetTokenGenerator,default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from django.template.loader import render_to_string

from rest_framework import mixins, viewsets, status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.serializers import UserSerializer, EmailSerializer, ChangePasswordSerializer, PasswordTokenSerializer
from apps.users.models import User
from apps.commons.constants import *


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
    An Api View which provides a method to request a password reset token based on an e-mail address
    """
    permission_classes = (AllowAny,)
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
            return Response({'data': 'Link has been sent to the valid email address', 'status': status.HTTP_200_OK})

        token = PasswordResetTokenGenerator.make_token(
            default_token_generator, user)

        reset_url = '{}/{}/{}/'.format(USER_CONSTANTS["PASSWORD_RESET_CONFIRM_URL"], user.id, token)
        
        ctx = {
            'name': user.get_short_name(),
            'reset_url': reset_url,
        } 
        send_mail(
            'Password Reset Email',
            render_to_string('reset_password_email.txt', ctx),
            'manager@ddm.com',
            [email],
            fail_silently=True,
            html_message=render_to_string('reset_password_email.html', ctx),
        )

        return Response({'data': 'Link has been sent to the valid email address','status': status.HTTP_200_OK})


class ResetPasswordTokenVerification(GenericAPIView):
    """
    An Api View which checks whether token is valid or not
    """
    permission_classes = (AllowAny,)
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        print "Hello"
        user = self.get_object()
        token = self.kwargs.get('token')
        if not PasswordResetTokenGenerator.check_token(default_token_generator, user, token):
            return Response({'data': 'Invalid token', 'status': status.HTTP_400_BAD_REQUEST})
        print "Valid token"    
        return Response({'status': status.HTTP_200_OK})


class ResetPasswordConfirm(GenericAPIView):
    """
    An Api View which provides a method to reset a password based on a unique token
    """
    permission_classes = (AllowAny,)
    serializer_class = PasswordTokenSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data['password']
        
        token = self.kwargs.get('token')
        user = self.get_object()

        if not PasswordResetTokenGenerator.check_token(default_token_generator, user, token):
            return Response({'data': 'Token not Valid', 'status': status.HTTP_400_BAD_REQUEST})

        user.set_password(password)
        user.save()

        return Response({'data': 'Password set successfully', 'status': status.HTTP_200_OK})
