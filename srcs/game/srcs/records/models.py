from django.db import models


class Game(models.Model):
    TYPE_CHOICES = (('1V1', '1v1'), ('TOURNAMENT', 'Tournament'))

    player_one = models.CharField(max_length=10)
    player_two = models.CharField(max_length=10)
    player_one_score = models.IntegerField()
    player_two_score = models.IntegerField()
    time = models.DateTimeField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='1v1')

    class Meta:
        app_label = "records"
        unique_together = ['player_one', 'player_two', 'player_one_score', 'player_two_score', 'time', 'type']


class Tournament(models.Model):
    game_one = models.ForeignKey(Game, related_name='game_one', on_delete=models.CASCADE)
    game_two = models.ForeignKey(Game, related_name='game_two', on_delete=models.CASCADE)
    game_three = models.ForeignKey(Game, related_name='game_three', on_delete=models.CASCADE)
    username = models.CharField(max_length=10)

    class Meta:
        unique_together = ['game_one', 'game_two', 'game_three', 'username']
