from rest_framework import generics

from users.models import User
from .serializers import UserSerializer


class UserDetailAPI(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
