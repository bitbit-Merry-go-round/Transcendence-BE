from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView, status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token

from .models import User, Friend
from .serializers import (
    UserDetailSerializer,
    UserUpdateSerializer,
    FriendListSerializer,
    FriendDetailSerializer,
    UserRegisterSerializer,
    UserLoginSerializer
)


class UserRegisterAPIView(APIView):
    def post(self, request: Request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token: Token = TokenObtainPairSerializer.get_token(user)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register successs",
                    "token": {
                        "access": str(token.access_token),
                        "refresh": str(token),
                    },
                },
                status=status.HTTP_200_OK,
            )
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    def post(self, request: Request):
        token_serializer = TokenObtainPairSerializer(data=request.data)
        if token_serializer.is_valid():
            user = token_serializer.user
            serializer = UserLoginSerializer(user)
            return Response(
                {
                    "user": serializer.data,
                    "message": "login success",
                    "token": token_serializer.validated_data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(token_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserDetailSerializer
        if self.request.method == 'PATCH':
            return UserUpdateSerializer

    http_method_names = ['get', 'patch']


class FriendListAPI(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['from_user'] = self.kwargs['from_user']
        return context

    def get_queryset(self):
        from_user = self.kwargs['from_user']
        queryset = Friend.objects.filter(from_user=from_user)
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FriendListSerializer
        if self.request.method == 'POST':
            return FriendDetailSerializer

    http_method_names = ['get', 'post']


class MultipleFieldLookupMixin(object):
    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]
        return get_object_or_404(queryset, **filter)


class FriendDeleteAPI(MultipleFieldLookupMixin, generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Friend.objects.all()
    serializer_class = FriendDetailSerializer
    lookup_fields = ('from_user', 'to_user')

    http_method_names = ['delete']
