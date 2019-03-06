from __future__ import unicode_literals
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import make_password

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apps.users.models import User


class UserCreateTest(APITestCase):
    valid_data = {
        "email": "jatin270@gmail.com",
        "password": "jtg12345",
        "first_name": "jatin",
        "last_name": "sharma",
        "user_type": 2,
    }

    url = reverse("users:users")
    url1 = reverse("users:login")
    
    def setUp(self):
        password1 = make_password("jatin123")
        self.user = User.objects.create(email="jatin70@gmail.com", password=password1, first_name="jatin", last_name="sharma")
        
    def test_can_create_user(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], 'jatin270@gmail.com')
        self.assertEqual(response.data['first_name'], 'jatin')
        self.assertEqual(response.data['last_name'], 'sharma')
        self.assertEqual(response.data['user_type'], 2)
    
    def test_can_check_unique_email(self):
        user_data = {"email": "jatin70@gmail.com", "password": "jtg12345", "first_name": "jatin", "last_name": "sharma", "user_type": 2, } 
        response = self.client.post(self.url, user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_get_user_deatils(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, {
                                            'id': self.user.id,
                                            'email': self.user.email,
                                            'first_name': self.user.first_name,
                                            'last_name': self.user.last_name,
                                            'user_type': self.user.user_type,
                                            })
    

class UserAuthenticationTest(APITestCase):

    valid_user = {
            "username": "jatin70@gmail.com",
            "password": "jatin123",
    }

    def setUp(self):
        password1 = make_password("jatin123")
        self.user = User.objects.create(email="jatin70@gmail.com", password=password1, first_name="jatin", last_name="sharma")

    url = reverse("users:login")
    url1 = reverse("users:logout")

    def test_can_check_login(self):
        response = self.client.post(self.url, self.valid_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_check_logout(self):
        self.client.force_authenticate(user=self.user)
        token = Token.objects.create(user=self.user)
        response = self.client.delete(self.url1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
