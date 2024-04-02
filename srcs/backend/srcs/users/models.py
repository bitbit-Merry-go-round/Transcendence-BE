import base64

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


def get_default_avatar(image_path):
    with open(image_path, 'rb') as f:
        image_b64 = base64.b64encode(f.read())
        return base64.decodebytes(image_b64)


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
            password=password,
            is_staff=True,
            is_superuser=True,
            **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    STATUS_CHOICES = (('OFFLINE', 'Offline'), ('ONLINE', 'Online'), ('GAMING', 'Gaming'))

    username = models.CharField(max_length=10, unique=True)
    avatar = models.BinaryField(default=get_default_avatar('static/avatar.jpg'))
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default='ONLINE')
    message = models.TextField(blank=True, default='')
    wins = models.IntegerField(default=0)
    loses = models.IntegerField(default=0)
    is_staff = models.BooleanField(default=False)

    password = models.CharField(null=True)

    objects = UserManager()

    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username

    class Meta:
        app_label = "users"


class Friend(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['from_user', 'to_user']
