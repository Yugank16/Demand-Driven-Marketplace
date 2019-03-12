from __future__ import unicode_literals

from django.contrib.auth.tokens import PasswordResetTokenGenerator, default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render



from rest_framework import mixins, viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.serializers import UserSerializer, EmailSerializer
from apps.users.models import User


class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """
    API for signup and get user details
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [AllowAny, ]
        return super(UserViewSet, self).get_permissions()

    def get_object(self):
        return self.request.user


class Logout(APIView):
    """
    Api For Logout 
    """

    def delete(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class ResetPasswordRequestToken(APIView):
    """
    An Api View which provides a method to request a password reset token based on an e-mail address
    Sends a signal reset_password_token_created when a reset token was created
    """
    permission_classes = (AllowAny,)
    serializer_class = EmailSerializer

    default_token_generator = PasswordResetTokenGenerator()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        user = User.objects.get(email=email)

        active_user_found = False
        if user:
            active_user_found = True

        if not active_user_found:
            raise ValidationError({
                'email': [(
                    "There is no active user associated with this e-mail address or the password can not be changed")],
            })

        token = PasswordResetTokenGenerator.make_token(
            default_token_generator, user)

        
        send_mail(
            'Password Reset Link',
            'Go to the following link to set a new password.{}'.format(),
            'from@example.com',
            [email],
            fail_silently=False,
        )

        return Response({'status': 'OK'})
