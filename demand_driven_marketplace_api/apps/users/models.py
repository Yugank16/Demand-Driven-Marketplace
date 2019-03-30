from __future__ import unicode_literals

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models

from apps.commons.constants import *


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),     
            
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    User Model To Store User Details
    """
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=USER_CONSTANTS["FIRST_NAME_MAX_LENGTH"])
    last_name = models.CharField(max_length=USER_CONSTANTS["LAST_NAME_MAX_LENGTH"], blank=True)
    balance = models.IntegerField(null=True)
    GENDER_CHOICES = (
        (USER_CONSTANTS["M"], 'MALE'),
        (USER_CONSTANTS["F"], 'FEMALE'),
        (USER_CONSTANTS["O"], 'OTHERS'),
    )
    gender = models.CharField(max_length=USER_CONSTANTS["GENDER"], choices=GENDER_CHOICES, null=True)
    profile_photo = models.ImageField(upload_to='profile_photo/', null=True)
    birth_date = models.DateField(null=True)
    phone_regex = RegexValidator(regex=r'^[6-9]{1}\d{9}$', message="Phone number must contain 10 digits.")
    phone_number = models.CharField(max_length=USER_CONSTANTS["PHONE_NUMBER"], validators=[phone_regex, ], blank=True)
    USER_TYPE_CHOICES = (
        (1, 'Buyer'),
        (2, 'Seller'),
        (3, 'Both'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=3)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.first_name

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True
 
    def __unicode__(self):
        return '{}'.format(self.first_name)

