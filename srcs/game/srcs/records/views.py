import environ
import jwt
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Game, Tournament
from .serializers import (
    GameSerializer,
    TournamentSerializer,
)

env = environ.Env()
environ.Env.read_env()


class OneOnOneGameAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]

    serializer_class = GameSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()

        token = self.request.headers.get("Authorization")
        bearer, _, token = token.partition(' ')
        payload = jwt.decode(jwt=token, key=env("SECRET_KEY"), algorithms=['HS256'])

        context["auth_user"] = payload.get("user_id")
        context["username"] = self.kwargs["username"]
        return context

    def get_queryset(self):
        username = self.kwargs["username"]
        queryset = Game.objects.filter(player_one=username, type='1v1')
        return queryset

    http_method_names = ['get', 'post', 'options']


class TournamentAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["username"] = self.kwargs["username"]
        return context

    def get_queryset(self):
        username = self.kwargs["username"]
        print(Tournament.objects.all())
        print(Game.objects.all())
        queryset = Tournament.objects.filter(username=username)
        print(queryset)
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TournamentSerializer
