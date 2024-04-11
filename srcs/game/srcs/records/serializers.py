from datetime import datetime

from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Game, Tournament


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

        if player_one != auth_user or player_two != "guest":
            raise ValidationError("invalid players")
        if player_one_score != win_score and player_two_score != win_score:
            raise ValidationError("invalid player scores")

        time = datetime.strptime(time, "%Y/%m/%d %H:%M:%S")
        time = timezone.make_aware(time)
        now = timezone.now()
        if now < time:
            raise ValidationError("invalid time")

        game = Game.objects.filter(
            player_one=player_one,
            player_two=player_two,
            player_one_score=player_one_score,
            player_two_score=player_two_score,
            time=time,
            type='1v1'
        ).first()

        if game is not None:
            raise ValidationError("duplicate game")

        return data

    class Meta:
        model = Game
        exclude = ['id', 'type']


class TournamentSerializer(serializers.ModelSerializer):
    winner = serializers.SerializerMethodField()
    time = serializers.DateTimeField(source='game_three.time')

    def get_winner(self, obj):
        last_game = obj.game_three
        if last_game.player_one_score > last_game.player_two_score:
            return last_game.player_one
        else:
            return last_game.player_two

    class Meta:
        model = Tournament
        fields = ['id', 'winner', 'time']


def validate_tournament_game(request_data, idx):
    win_score = 3

    player_one = request_data[idx]['player_one']
    player_two = request_data[idx]['player_two']
    player_one_score = request_data[idx]['player_one_score']
    player_two_score = request_data[idx]['player_two_score']
    time = request_data[idx]['time']

    if player_one == player_two:
        raise ValidationError("identical players")
    if player_one_score != win_score and player_two_score != win_score:
        raise ValidationError("invalid player scores")

    time = datetime.strptime(time, "%Y/%m/%d %H:%M:%S")
    time = timezone.make_aware(time)
    now = timezone.now()
    if now < time:
        raise ValidationError("invalid time")


def create_tournament_game(request_data, idx):
    player_one = request_data[idx]['player_one']
    player_two = request_data[idx]['player_two']
    player_one_score = request_data[idx]['player_one_score']
    player_two_score = request_data[idx]['player_two_score']
    time = request_data[idx]['time']
    time = datetime.strptime(time, "%Y/%m/%d %H:%M:%S")
    time = timezone.make_aware(time)

    game = Game.objects.filter(
        player_one=player_one,
        player_two=player_two,
        player_one_score=player_one_score,
        player_two_score=player_two_score,
        time=time,
        type='tournament'
    ).first()

    if game is None:
        return Game.objects.create(
            player_one=player_one,
            player_two=player_two,
            player_one_score=player_one_score,
            player_two_score=player_two_score,
            time=time,
            type='tournament'
        )

    else:
        return game


def get_game_winner(request_data, idx):
    player_one_score = request_data[idx]['player_one_score']
    player_two_score = request_data[idx]['player_two_score']

    if player_one_score > player_two_score:
        return request_data[idx]['player_one']
    else:
        return request_data[idx]['player_two']


class TournamentCreationSerializer(serializers.ModelSerializer):
    game_one = GameSerializer(read_only=True)
    game_two = GameSerializer(read_only=True)
    game_three = GameSerializer(read_only=True)

    def validate(self, data):
        username = self.context['username']
        request_data = self.context['request'].data

        validate_tournament_game(request_data, 0)
        validate_tournament_game(request_data, 1)
        validate_tournament_game(request_data, 2)

        game_one_time = request_data[0]['time']
        game_two_time = request_data[1]['time']
        game_three_time = request_data[2]['time']

        if game_one_time >= game_two_time or game_two_time >= game_three_time:
            raise ValidationError("invalid game times")

        winner_one = get_game_winner(request_data, 0)
        winner_two = get_game_winner(request_data, 1)
        if request_data[2]['player_one'] != winner_one or request_data[2]['player_two'] != winner_two:
            raise ValidationError("invalid game players")

        game_one = create_tournament_game(request_data, 0)
        game_two = create_tournament_game(request_data, 1)
        game_three = create_tournament_game(request_data, 2)

        tournament = Tournament.objects.filter(
            game_one=game_one,
            game_two=game_two,
            game_three=game_three,
            username=username
        ).first()

        if tournament is not None:
            raise ValidationError("duplicate tournament")

        return data

    def create(self, validated_data):
        username = self.context['username']
        request_data = self.context['request'].data

        game_one = create_tournament_game(request_data, 0)
        game_two = create_tournament_game(request_data, 1)
        game_three = create_tournament_game(request_data, 2)

        tournament = Tournament.objects.create(
            game_one=game_one,
            game_two=game_two,
            game_three=game_three,
            username=username
        )

        return tournament

    class Meta:
        model = Tournament
        fields = ['game_one', 'game_two', 'game_three']
