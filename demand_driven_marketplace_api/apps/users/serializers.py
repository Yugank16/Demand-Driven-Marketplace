from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
import django.contrib.auth.password_validation as validators

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
        fields = ('id', 'email', 'password', 'profile_photo', 'birth_date', 'gender', 'phone_number', 'first_name', 'last_name', 'user_type', 'token')
    
    def validate_password(self, password):
        return make_password(password)

    def create(self, validated_data):
        print validated_data
        validated_data['balance'] = CONSTANTS['INITIAL_BALANCE']
        user = User.objects.create(**validated_data)
        token = Token.objects.create(user=user)
        user.token = token.key
        return user


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordTokenSerializer(serializers.Serializer):
    password = serializers.CharField()
    token = serializers.CharField()


class ChangePasswordSerializer(serializers.ModelSerializer):

    password = serializers.CharField()
    new_password = serializers.CharField(write_only=True) 

    class Meta(object):
        model = User
        fields = ('password', 'new_password')

    def validate(self, data):
        validators.validate_password(password=data['password'], user=self.instance)
        if(data['password'] == data['new_password']):
            raise ValidationError('Password can not be same as old password')
        return data
    
    def update(self, instance, validated_data):
        print validated_data
        validated_data['password'] = make_password(validated_data['new_password'])
        validated_data.pop('new_password')
        print validated_data
        instance = super(ChangePasswordse, self).update(instance, validated_data)
        return instance




