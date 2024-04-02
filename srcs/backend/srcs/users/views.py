from json import JSONDecodeError

import requests
from django.conf import settings
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import status

from .models import User, Friend
from .serializers import (
    UserDetailSerializer,
    UserUpdateSerializer,
    FriendListSerializer,
    FriendDetailSerializer,
)

FOURTYTWO_CALLBACK_URI = 'http%3A%2F%2F127.0.0.1%3A8080%2Flogin'


def fourtytwo_callback(request):
    client_id = settings.FOURTYTWO_CLIENT_ID
    client_secret = settings.FOURTYTWO_CLIENT_SECRET
    code = request.GET.get("code")

    token_response = requests.post(
        f"https://api.intra.42.fr/oauth/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={code}&redirect_uri={FOURTYTWO_CALLBACK_URI}")
    token_response_json = token_response.json()

    error = token_response_json.get("error", None)
    if error is not None:
        raise JSONDecodeError(error)

    access_token = token_response_json.get("access_token")
    refresh_token = token_response_json.get("refresh_token")

    profile_response = requests.get(
        "https://api.intra.42.fr/v2/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response_status = profile_response.status_code

    if response_status != 200:
        return JsonResponse({
            'message': 'Bad Request'
        }, status=response_status)

    profile_response_json = profile_response.json()
    username = profile_response_json.get("login")

    try:
        user = User.objects.get(username=username)
        return JsonResponse({
            'access_token': access_token,
            'refresh_token': refresh_token
        }, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        user = User(username=username)
        user.set_unusable_password()
        user.save()
        return JsonResponse({
            'access_token': access_token,
            'refresh_token': refresh_token
        }, status=status.HTTP_201_CREATED)


class UserSearchAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        query = self.request.query_params
        context['user'] = User.objects.filter(username=query.get('search')).first()
        return context

    def get_object(self):
        queryset = self.get_queryset()
        query = self.request.query_params
        user = get_object_or_404(queryset, username=query.get('search'))
        return user

    http_method_names = ['get', 'options']


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

    def get_object(self):
        username = self.kwargs['username']
        user = User.objects.filter(username=username).first()
        return user

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserDetailSerializer
        if self.request.method == 'PATCH':
            return UserUpdateSerializer

    http_method_names = ['get', 'patch', 'options']


class FriendListAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['from_user'] = self.kwargs['from_user']
        return context

    def get_queryset(self):
        from_user = self.kwargs['from_user']
        user = User.objects.filter(username=from_user).first()
        queryset = Friend.objects.filter(from_user=user)
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FriendListSerializer
        if self.request.method == 'POST':
            return FriendDetailSerializer

    http_method_names = ['get', 'post', 'options']


class MultipleFieldLookupMixin(object):
    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter = {}
        for field in self.lookup_fields:
            username = self.kwargs[field]
            user = User.objects.filter(username=username).first()
            filter[field] = user.pk
        return get_object_or_404(queryset, **filter)


class FriendDeleteAPIView(MultipleFieldLookupMixin, generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Friend.objects.all()
    serializer_class = FriendDetailSerializer
    lookup_fields = ('from_user', 'to_user')

    http_method_names = ['delete', 'options']
