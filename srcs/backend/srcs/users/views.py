from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import User, Friend
from .serializers import UserInitSerializer, UserDetailSerializer, UserUpdateSerializer, FriendListSerializer, \
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


class FriendListAPI(generics.ListCreateAPIView):
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
            return FriendSerializer

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
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer
    lookup_fields = ('from_user', 'to_user')

    http_method_names = ['delete']
