from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
import django.contrib.auth.password_validation as validators
from django.contrib.auth.hashers import check_password

from datetime import datetime, date
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from apps.users.constants import CONSTANTS
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    UserSerializer For Getting User Details ,Creating New User And Update User
    Profile
    """
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    class Meta(object):
        model = User
        fields = ('id', 'email', 'password', 'profile_photo', 'birth_date', 'gender', 'phone_number', 'first_name', 'last_name', 'user_type', 'token')
    
    def validate_password(self, password):
        return make_password(password)

    def validate_birth_date(self, value):
        if value >= date.today() :
            raise serializers.ValidationError({"birth_date": "Birth Date should be valid"})
        return value

    def validate(self, data):
        return data

    def create(self, validated_data):
        validated_data['balance'] = CONSTANTS['INITIAL_BALANCE']
        user = User.objects.create(**validated_data)
        token = Token.objects.create(user=user)
        user.token = token.key
        return user


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordTokenSerializer(serializers.Serializer):
    password = serializers.CharField()


class ChangePasswordSerializer(serializers.ModelSerializer):
    """
    Serializer to change password
    """
    password = serializers.CharField()
    new_password = serializers.CharField(write_only=True) 

    class Meta(object):
        model = User
        fields = ('password', 'new_password')

    def validate(self, data):
        if not (check_password(data['password'], self.instance.password)):
            raise ValidationError('Incorrect Old Password')
        if(data['password'] == data['new_password']):
            raise ValidationError('Password can not be same as old password')    
        return data    
    
    def update(self, instance, validated_data):
        validated_data['password'] = make_password(validated_data['new_password'])
        validated_data.pop('new_password')
        instance = super(ChangePasswordSerializer, self).update(instance, validated_data)
        return instance
