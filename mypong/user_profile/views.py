from rest_framework import generics

from users.models import User
from .serializers import UserProfileSerializer


class UserProfileAPI(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
