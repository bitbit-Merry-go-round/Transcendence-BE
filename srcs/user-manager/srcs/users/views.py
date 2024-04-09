import environ
import jwt
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny

from .models import User, Friend
from .serializers import (
    UserDetailSerializer,
    UserUpdateSerializer,
    FriendListSerializer,
    FriendCreationSerializer,
    UserLoginSerializer,
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
        context["username"] = User.objects.get(username=query.get("search"))
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
        username = self.kwargs["username"]
        user = User.objects.get(username=username)
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
        token = self.request.headers.get("Authorization")
        bearer, _, token = token.partition(' ')
        payload = jwt.decode(jwt=token, key=env("SECRET_KEY"), algorithms=['HS256'])
        context["auth_user"] = payload.get("user_id")
        context["username"] = context["auth_user"]
        return context

    def get_queryset(self):
        token = self.request.headers.get("Authorization")
        bearer, _, token = token.partition(' ')
        payload = jwt.decode(jwt=token, key=env("SECRET_KEY"), algorithms=['HS256'])
        from_user = payload.get("user_id")
        from_user = User.objects.get(username=from_user)
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
        from_user = self.kwargs["from_user"]
        to_user = self.kwargs["to_user"]
        from_user = User.objects.get(username=from_user)
        to_user = User.objects.get(username=to_user)
        obj = Friend.objects.get(from_user=from_user, to_user=to_user)
        return obj

    http_method_names = ['delete', 'options']


class UserCreationAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer
    queryset = User.objects.all()

    http_method_names = ['post', 'options']
