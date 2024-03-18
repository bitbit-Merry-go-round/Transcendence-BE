from rest_framework import generics, exceptions

from users.models import User
from .serializers import UserProfileSerializer, UserUpdateSerializer


class UserProfileAPI(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserProfileSerializer
        if self.request.method == 'PATCH':
            return UserUpdateSerializer

    http_method_names = ['get', 'patch']
