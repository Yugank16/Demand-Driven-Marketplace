from __future__ import unicode_literals
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import make_password

from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import User


class UserViewsetCreateTest(APITestCase):
    valid_data = {
        "email": "jatin270@gmail.com",
        "password": "jtg12345",
        "first_name": "jatin",
        "last_name": "sharma",
        "user_type": 2,
    }
    valid_user = {
            "username": "jatin70@gmail.com",
            "password": "jatin",
    }
    url = reverse("users:users")
    url1 = reverse("users:login")
    url2 = reverse("users:logout")
    
    def setUp(self):
        password1 = make_password("jatin")
        self.user = User.objects.create(email="jatin70@gmail.com", password=password1, first_name="jatin", last_name="sharma")
        self.user1 = User.objects.create(email="jatin170@gmail.com", password=password1, first_name="sharma", last_name="jatin")
        
    def test_can_create_user(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_check_login(self):
        response = self.client.post(self.url1, self.valid_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
   
    



