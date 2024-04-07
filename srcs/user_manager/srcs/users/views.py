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
