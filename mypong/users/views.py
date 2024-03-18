from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import User
from .serializers import UserInitSerializer, UserDetailSerializer, UserUpdateSerializer


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
