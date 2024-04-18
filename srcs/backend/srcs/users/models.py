from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("Users must have an username")

        user = self.model(username=username, **extra_fields)
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        return self.create_user(
            username=username,
            is_superuser=True,
            password=password,
            **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=10, unique=True)
    password = models.CharField(null=True)

    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    email_verified = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username

    class Meta:
        app_label = "users"
