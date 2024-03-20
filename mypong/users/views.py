from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import User, Friend
from .serializers import UserInitSerializer, UserDetailSerializer, UserUpdateSerializer, FriendListSerializer, \
    FriendCreationSerializer


@api_view(['GET'])
def HelloAPI(request):
    return Response("Hello!")


class UserCreationAPI(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserInitSerializer
    http_method_names = ['post']


class UserProfileAPI(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserDetailSerializer
        if self.request.method == 'PATCH':
            return UserUpdateSerializer

    http_method_names = ['get', 'patch']


class FriendListAPI(generics.ListCreateAPIView):
    def get_queryset(self):
        from_user = self.kwargs['from_user']
        queryset = Friend.objects.filter(from_user__exact=from_user)
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FriendListSerializer
        if self.request.method == 'POST':
            return FriendCreationSerializer

    http_method_names = ['get', 'post']
