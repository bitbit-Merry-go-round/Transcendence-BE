from datetime import datetime

from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Game


class GameSerializer(serializers.ModelSerializer):
    def validate(self, data):
        win_score = 3

        auth_user = self.context['auth_user']

        request_data = self.context['request'].data
        player_one = request_data.get('player_one')
        player_two = request_data.get('player_two')
        player_one_score = request_data.get('player_one_score')
        player_two_score = request_data.get('player_two_score')
        time = request_data.get('time')

        print(player_one)
        print(player_two)
        if player_one != auth_user or player_two != "guest":
            raise ValidationError("invalid players")
        if player_one_score != win_score and player_two_score != win_score:
            raise ValidationError("invalid player scores")

        time = datetime.strptime(time, "%Y/%m/%d %H:%M:%S")
        time = timezone.make_aware(time)
        now = timezone.now()
        if now < time:
            raise ValidationError("invalid time")

        return data

    class Meta:
        model = Game
        exclude = ['id', 'type']
