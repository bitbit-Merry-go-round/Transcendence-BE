import environ
import jwt
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny

from .models import Game, Tournament
from .serializers import (
    MyGameSerializer,
    GameSerializer,
    TournamentSimpleSerializer,
    TournamentDetailSerializer,
)

env = environ.Env()
environ.Env.read_env()


class MyOneOnOneGameAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]

    serializer_class = MyGameSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()

        token = self.request.headers.get("Authorization")
        bearer, _, token = token.partition(' ')
        payload = jwt.decode(jwt=token, key=env("SECRET_KEY"), algorithms=['HS256'])

        context["me"] = payload.get("user_id")

        return context

    def get_queryset(self):
        token = self.request.headers.get("Authorization")
        bearer, _, token = token.partition(' ')
        payload = jwt.decode(jwt=token, key=env("SECRET_KEY"), algorithms=['HS256'])

        me = payload.get("user_id")
        queryset = Game.objects.filter(player_one=me, player_two="guest", type='1v1').order_by("time")

        return queryset

    http_method_names = ['get', 'post', 'options']


class MyTournamentAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        context = super().get_serializer_context()

        token = self.request.headers.get("Authorization")
        bearer, _, token = token.partition(' ')
        payload = jwt.decode(jwt=token, key=env("SECRET_KEY"), algorithms=['HS256'])

        context["me"] = payload.get("user_id")

        return context

    def get_queryset(self):
        token = self.request.headers.get("Authorization")
        bearer, _, token = token.partition(' ')
        payload = jwt.decode(jwt=token, key=env("SECRET_KEY"), algorithms=['HS256'])

        me = payload.get("user_id")
        queryset = Tournament.objects.filter(username=me)

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TournamentSimpleSerializer
        if self.request.method == 'POST':
            return TournamentDetailSerializer

    http_method_names = ['get', 'post', 'options']


class UserOneOnOneGameAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]

    serializer_class = GameSerializer

    def get_queryset(self):
        username = self.kwargs["username"]
        queryset = Game.objects.filter(player_one=username, player_two="guest", type='1v1')
        return queryset

    http_method_names = ['get', 'options']


class UserTournamentAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]

    serializer_class = TournamentSimpleSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["username"] = self.kwargs["username"]
        return context

    def get_queryset(self):
        username = self.kwargs["username"]
        queryset = Tournament.objects.filter(username=username)
        return queryset

    http_method_names = ['get', 'options']


class TournamentDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]

    queryset = Tournament.objects.all()
    serializer_class = TournamentDetailSerializer

    def get_object(self):
        queryset = self.get_queryset()
        id = self.kwargs["tournament_id"]
        tournament = get_object_or_404(queryset, id=id)
        return tournament

    http_method_names = ['get', 'options']
