from __future__ import unicode_literals
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import make_password

from rest_framework import status
from rest_framework.authtoken.models import Token
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
            "password": "jatin123",
    }
    url = reverse("users:users")
    url1 = reverse("users:login")
    url2 = reverse("users:logout")
    
    def setUp(self):
        password1 = make_password("jatin123")
        self.user = User.objects.create(email="jatin70@gmail.com", password=password1, first_name="jatin", last_name="sharma")
        
    def test_can_create_user(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_check_login(self):
        response = self.client.post(self.url1, self.valid_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_can_get_user_deatils(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_check_logout(self):
        self.client.force_authenticate(user=self.user)
        token = Token.objects.create(user=self.user)
        response = self.client.delete(self.url2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_can_check_unique_email(self):
        user_data = {"email": "jatin70@gmail.com", "password": "jtg12345", "first_name": "jatin", "last_name": "sharma", "user_type": 2, } 
        response = self.client.post(self.url, user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_can_check_password_validation(self):
        # test for password lenght too short
        user_data = {"email": "jatin70@gmail.com", "password": "j", "first_name": "jatin", "last_name": "sharma", "user_type": 2, } 
        response = self.client.post(self.url, user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # test for password length too large
        user_data = {"email": "jatin70@gmail.com", "password": "jqwertyuiopoiuytrewqwerqweqqqweqeqeqwqwwq", "first_name": "jatin", "last_name": "sharma", "user_type": 2, } 
        response = self.client.post(self.url, user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



    
   
    



