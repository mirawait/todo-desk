import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError("Username cannot be blank")
        if email is None:
            raise TypeError("Email cannot be blank")
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password):
        if password is None:
            raise TypeError("Enter password")
        user = self.create_superuser(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
