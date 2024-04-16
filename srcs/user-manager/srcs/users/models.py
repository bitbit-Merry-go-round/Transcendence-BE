import base64

from django.db import models


def get_default_avatar(image_path):
    with open(image_path, 'rb') as f:
        image_b64 = base64.b64encode(f.read())
        return base64.decodebytes(image_b64)


class User(models.Model):
    STATUS_CHOICES = (('OFFLINE', 'Offline'), ('ONLINE', 'Online'))

    username = models.CharField(max_length=10, unique=True)
    avatar = models.BinaryField(default=get_default_avatar('static/avatar.jpg'))
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default='OFFLINE')
    message = models.TextField(blank=True, default='')
    wins = models.IntegerField(default=0)
    loses = models.IntegerField(default=0)
    friends = models.ManyToManyField('self', symmetrical=False, through='Friend',
                                     through_fields=('from_user', 'to_user'))

    def __str__(self):
        return self.username

    class Meta:
        app_label = "users"


class Friend(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['from_user', 'to_user']
