from json import JSONDecodeError

import requests
from django.conf import settings
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Friend
from .serializers import (
    UserDetailSerializer,
    UserUpdateSerializer,
    FriendListSerializer,
    FriendCreationSerializer,
    AuthUserSerializer,
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
        token = RefreshToken.for_user(user)
        refresh = str(token)
        access = str(token.access_token)

        return JsonResponse({
            'access': access,
            'refresh': refresh,
        }, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        new_user = User(username=username)
        new_user.set_unusable_password()
        new_user.save()
        token = RefreshToken.for_user(new_user)
        refresh = str(token)
        access = str(token.access_token)

        return JsonResponse({
            'access': access,
            'refresh': refresh,
        }, status=status.HTTP_201_CREATED)


class UserSearchAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        query = self.request.query_params
        context['user'] = User.objects.get(username=query.get('search'))
        return context

    def get_object(self):
        queryset = self.get_queryset()
        query = self.request.query_params
        user = get_object_or_404(queryset, username=query.get('search'))
        return user

    http_method_names = ['get', 'options']


class MyProfileAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    queryset = User.objects.all()

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AuthUserSerializer
        if self.request.method == 'PATCH':
            return UserUpdateSerializer

    http_method_names = ['get', 'patch', 'options']


class UserProfileAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

    def get_object(self):
        username = self.kwargs['username']
        user = User.objects.filter(username=username).first()
        return user

    http_method_names = ['get', 'options']


class MyFriendAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

    def get_queryset(self):
        from_user = self.request.user
        queryset = Friend.objects.filter(from_user=from_user)
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FriendListSerializer
        if self.request.method == 'POST':
            return FriendCreationSerializer

    http_method_names = ['get', 'post', 'options']


class FriendDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    queryset = Friend.objects.all()
    serializer_class = FriendListSerializer

    def get_object(self):
        from_user = self.request.user
        username = self.kwargs['to_user']
        to_user = User.objects.get(username=username)
        obj = Friend.objects.get(from_user=from_user, to_user=to_user)
        return obj

    http_method_names = ['delete', 'options']
