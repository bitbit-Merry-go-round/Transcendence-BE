import environ
import jwt
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny

from .models import User, Friend
from .serializers import (
    UserInitSerializer,
    UserDetailSerializer,
    UserUpdateSerializer,
    FriendListSerializer,
    FriendCreationSerializer,
)

env = environ.Env()
environ.Env.read_env()


class UserSearchAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]

    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()

        query = self.request.query_params
        context["username"] = query.get("search")

        token = self.request.headers.get("Authorization")
        bearer, _, token = token.partition(' ')
        payload = jwt.decode(jwt=token, key=env("SECRET_KEY"), algorithms=['HS256'])
        context["auth_user"] = payload.get("user_id")

        return context

    def get_object(self):
        queryset = self.get_queryset()
        query = self.request.query_params
        user = get_object_or_404(queryset, username=query.get('search'))
        return user

    http_method_names = ['get', 'options']


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [AllowAny]

    queryset = User.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()

        context["username"] = self.kwargs["username"]

        token = self.request.headers.get("Authorization")
        bearer, _, token = token.partition(' ')
        payload = jwt.decode(jwt=token, key=env("SECRET_KEY"), algorithms=['HS256'])
        context["auth_user"] = payload.get("user_id")

        return context

    def get_object(self):
        queryset = self.get_queryset()
        username = self.kwargs["username"]
        user = get_object_or_404(queryset, username=username)
        return user

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserDetailSerializer
        if self.request.method == 'PATCH':
            return UserUpdateSerializer

    http_method_names = ['get', 'patch', 'options']


class MyFriendAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        context = super().get_serializer_context()

        context["username"] = self.kwargs["username"]

        token = self.request.headers.get("Authorization")
        bearer, _, token = token.partition(' ')
        payload = jwt.decode(jwt=token, key=env("SECRET_KEY"), algorithms=['HS256'])
        context["auth_user"] = payload.get("user_id")

        return context

    def get_queryset(self):
        username = self.kwargs["username"]
        from_user = get_object_or_404(User.objects.all(), username=username)
        queryset = Friend.objects.filter(from_user=from_user)
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FriendListSerializer
        if self.request.method == 'POST':
            return FriendCreationSerializer

    http_method_names = ['get', 'post', 'options']


class FriendDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [AllowAny]

    queryset = Friend.objects.all()
    serializer_class = FriendListSerializer

    def get_object(self):
        queryset = self.get_queryset()

        from_user = self.kwargs["from_user"]
        to_user = self.kwargs["to_user"]

        from_user = get_object_or_404(User.objects.all(), username=from_user)
        to_user = get_object_or_404(User.objects.all(), username=to_user)

        friend = get_object_or_404(queryset, from_user=from_user, to_user=to_user)
        return friend

    http_method_names = ['delete', 'options']


class UserCreationAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]

    queryset = User.objects.all()
    serializer_class = UserInitSerializer

    http_method_names = ['post', 'options']
