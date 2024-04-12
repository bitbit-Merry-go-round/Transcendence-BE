import environ
import jwt
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import User, Friend
from .serializers import (
    MyProfileSerializer,
    MyProfileUpdateSerializer,
    MyFriendSerializer,
    UserProfileSerializer,
    UserInitSerializer,
)

env = environ.Env()
environ.Env.read_env()


class MyProfileAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [AllowAny]

    queryset = User.objects.all()

    def get_object(self):
        queryset = self.get_queryset()

        token = self.request.headers.get("Authorization")
        bearer, _, token = token.partition(' ')
        payload = jwt.decode(jwt=token, key=env("SECRET_KEY"), algorithms=['HS256'])

        username = payload.get("user_id")
        me = get_object_or_404(queryset, username=username)

        return me

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MyProfileSerializer
        if self.request.method == 'PATCH':
            return MyProfileUpdateSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        wins = request.data.pop('wins', None)
        loses = request.data.pop('loses', None)

        data = request.data
        if wins is not None:
            data['wins'] = wins + instance.wins
        if loses is not None:
            data['loses'] = loses + instance.loses

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    http_method_names = ['get', 'patch', 'options']


class MyFriendAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]

    serializer_class = MyFriendSerializer

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

        username = payload.get("user_id")
        me = get_object_or_404(User.objects.all(), username=username)

        queryset = Friend.objects.filter(from_user=me)

        return queryset

    http_method_names = ['get', 'post', 'options']


class MyFriendDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [AllowAny]

    queryset = Friend.objects.all()
    serializer_class = MyFriendSerializer

    def get_object(self):
        queryset = self.get_queryset()

        token = self.request.headers.get("Authorization")
        bearer, _, token = token.partition(' ')
        payload = jwt.decode(jwt=token, key=env("SECRET_KEY"), algorithms=['HS256'])

        from_user = payload.get("user_id")
        to_user = self.kwargs["to_user"]

        from_user = get_object_or_404(User.objects.all(), username=from_user)
        to_user = get_object_or_404(User.objects.all(), username=to_user)

        friend = get_object_or_404(queryset, from_user=from_user, to_user=to_user)
        return friend

    http_method_names = ['delete', 'options']


class UserProfileAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()

        token = self.request.headers.get("Authorization")
        bearer, _, token = token.partition(' ')
        payload = jwt.decode(jwt=token, key=env("SECRET_KEY"), algorithms=['HS256'])

        context["me"] = payload.get("user_id")
        context["username"] = self.kwargs["username"]

        return context

    def get_object(self):
        queryset = self.get_queryset()
        username = self.kwargs["username"]
        user = get_object_or_404(queryset, username=username)
        return user

    http_method_names = ['get', 'options']


class UserSearchAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()

        token = self.request.headers.get("Authorization")
        bearer, _, token = token.partition(' ')
        payload = jwt.decode(jwt=token, key=env("SECRET_KEY"), algorithms=['HS256'])
        context["me"] = payload.get("user_id")

        query = self.request.query_params
        context["username"] = query.get("search")

        return context

    def get_object(self):
        queryset = self.get_queryset()
        query = self.request.query_params
        user = get_object_or_404(queryset, username=query.get('search'))
        return user

    http_method_names = ['get', 'options']


class UserCreationAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]

    queryset = User.objects.all()
    serializer_class = UserInitSerializer

    http_method_names = ['post', 'options']
