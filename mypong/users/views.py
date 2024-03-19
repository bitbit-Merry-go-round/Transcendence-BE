from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import User, Friend
from .serializers import UserInitSerializer, UserDetailSerializer, UserUpdateSerializer, \
    FriendSerializer


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


class FriendListAPI(generics.ListAPIView):
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer


class FriendCreationAPI(generics.CreateAPIView):
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer
    http_method_names = ['post']

# class FriendDeleteAPI(generics.DestroyAPIView):
#     queryset = Friend.objects.all()

# def deleeter(self, request, *args, **kwargs):
#     # user = request.user
#     user = self.kwargs.get('from_user')
#     friend_id = self.kwargs.get('to_user')
#     friend = Friend.objects.filter(from_user_id=user, to_user_id=friend_id).frist()
#
#     try:
#         Friend.objects.filter(from_user_id=user.uid).remove(friend_id)
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     except:
#         return Response(status=status.HTTP_404_NOT_FOUND)
