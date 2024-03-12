from django.db import models


class User(models.Model):
    friends = models.ManyToManyField("User", blank="True")

    STATUS_CHOICES = (
        ('OF', 'Offline'),
        ('ON', 'Online'),
        ('GA', 'Gaming')
    )

    uid = models.CharField(
        max_length=10,
        primary_key=True
    )
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default='OF'
    )
    message = models.TextField(
        blank=True,
        default=''
    )
    wins = models.IntegerField(
        default=0
    )
    loses = models.IntegerField(
        default=0
    )

    def __str__(self):
        return self.uid


class Friend(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)

    def __str__(self):
        return self.from_user, self.to_user
