from django.db import models


class User(models.Model):
    STATUS_CHOICES = (
        ('OF', 'Offline'),
        ('ON', 'Online'),
        ('GA', 'Gaming'),
    )

    id = models.CharField(
        max_length=10,
        primary_key=True,
    )
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default='OF',
    )
    message = models.TextField(
        blank=True,
    )
    wins = models.IntegerField(
        default=0,
    )
    loses = models.IntegerField(
        default=0,
    )

    def __str__(self):
        return self.id
