from __future__ import unicode_literals

from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.db import models

from users.constants import CONSTANTS

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
    email = models.EmailField(max_length=CONSTANTS["TEXT_SIZE_MEDIUM"], unique=True)
    name = models.CharField(max_length=CONSTANTS["TEXT_SIZE_MEDIUM"])
    phone_number = models.IntegerField()
    balance =  models.IntegerField()
    USER_TYPE_CHOICES = (
        (1, 'Buyer'),
        (2, 'Seller'),
        (3, 'Both'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

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
        return '{}'.format(self.name)
