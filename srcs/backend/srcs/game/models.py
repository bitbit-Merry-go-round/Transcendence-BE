from django.db import models


class Game(models.Model):
    player_one = models.CharField(max_length=10)
    player_two = models.CharField(max_length=10)
    player_one_score = models.IntegerField(default=0)
    player_two_score = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("player_one", "player_two")


class GameInfo(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    paddle_pox_x = models.FloatField(default=0)
    paddle_pox_y = models.FloatField(default=0)

    ball_pos_x = models.FloatField(default=0)
    ball_pos_y = models.FloatField(default=0)
