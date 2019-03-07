from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from apps.users.constants import CONSTANTS
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    UserSerializer For Getting User Details And Creating New User 
    """
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    class Meta(object):
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'user_type', 'token')

    def create(self, validated_data):
        print validated_data
        validated_data['balance'] = CONSTANTS['INITIAL_BALANCE']
        user = User.objects.create(**validated_data)
        print user
        token = Token.objects.create(user=user)
        user.token = token.key
        return user


