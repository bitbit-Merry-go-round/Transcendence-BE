import environ
import jwt
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Game, Tournament
from .serializers import (
    GameSerializer,
    TournamentSerializer,
    TournamentCreationSerializer,
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


def convert_to_dict(lst):
    res_dict = {}
    for i in range(len(lst)):
        res_dict[i] = lst[i]
    return res_dict


class TournamentAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["username"] = self.kwargs["username"]
        return context

    def get_queryset(self):
        username = self.kwargs["username"]
        queryset = Tournament.objects.filter(username=username)
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TournamentSerializer
        if self.request.method == 'POST':
            return TournamentCreationSerializer

    def create(self, request, *args, **kwargs):
        data = convert_to_dict(request.data)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(request.data, status=status.HTTP_201_CREATED, headers=headers)

    http_method_names = ['get', 'post', 'options']
