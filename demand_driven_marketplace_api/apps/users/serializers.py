from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from apps.users.constants import CONSTANTS
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    class Meta(object):
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'user_type', 'token')

    def validate(seld, data):
        if len(data['password']) < CONSTANTS['PASSWORD_MIN_LENGTH']:
            raise ValidationError('Password too Short.It must contain atleast {} characters.'.format(CONSTANTS['PASSWORD_MIN_LENGTH']))
        if len(data['password']) > CONSTANTS['PASSWORD_MAX_LENGTH']:
            raise ValidationError('Password too long.It must contain less than {} characters.'.format(CONSTANTS['PASSWORD_MAX_LENGTH']))
        if len(data['first_name']) < CONSTANTS['FIRST_NAME_MIN_LENGTH']:
            raise ValidationError('First name too Short.It must contain atleast {} characters.'.format(CONSTANTS['FIRST_NAME_MIN_LENGTH']))
        if len(data['first_name']) > CONSTANTS['FIRST_NAME_MAX_LENGTH']:
            raise ValidationError('First name too Long.It must contain less than {} characters.'.format(CONSTANTS['FIRST_NAME_MAX_LENGTH'])) 
        if len(data['last_name']) > CONSTANTS['LAST_NAME_MAX_LENGTH']:
            raise ValidationError('Last name too Long.It must contain less than {} characters.'.format(CONSTANTS['LAST_NAME_MAX_LENGTH']))   
        data['password'] = make_password(data['password'])
        return data

    def create(self, validated_data):
        print validated_data
        validated_data['balance'] = CONSTANTS['INITIAL_BALANCE']
        user = User.objects.create(**validated_data)
        print user
        token = Token.objects.create(user=user)
        user.token = token.key
        return user
