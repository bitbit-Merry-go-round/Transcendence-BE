from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


@api_view(['GET'])
def HelloAPI(request):
    return Response("Hello!")


class UserCreationAPI(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailAPI(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
