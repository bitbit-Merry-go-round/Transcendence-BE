from json import JSONDecodeError

import requests
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import status

from fourtytwo.views import FourtytwoOAuth2Adapter

from .models import User, Friend
from .serializers import (
    UserDetailSerializer,
    UserUpdateSerializer,
    FriendListSerializer,
    FriendDetailSerializer,
)

FOURTYTWO_CALLBACK_URI = 'http%3A%2F%2F127.0.0.1%3A8000%2Fusers%2F42%2Fcallback'


def fourtytwo_login(request):
    client_id = settings.SOCIAL_AUTH_FOURTYTWO_CLIENT_ID
    return redirect(
        f"https://api.intra.42.fr/oauth/authorize?client_id={client_id}&redirect_uri={FOURTYTWO_CALLBACK_URI}&response_type=code")


def fourtytwo_callback(request):
    client_id = settings.SOCIAL_AUTH_FOURTYTWO_CLIENT_ID
    client_secret = settings.SOCIAL_AUTH_FOURTYTWO_CLIENT_SECRET
    code = request.GET.get("code")

    # code로 access token 요청
    token_response = requests.post(
        f"https://api.intra.42.fr/oauth/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={code}&redirect_uri={FOURTYTWO_CALLBACK_URI}")
    token_response_json = token_response.json()

    # 에러 발생 시 중단
    error = token_response_json.get("error", None)
    if error is not None:
        raise JSONDecodeError(error)

    access_token = token_response_json.get("access_token")
    print(access_token)
    # access token으로 42 프로필 요청
    profile_response = requests.get(
        "https://api.intra.42.fr/v2/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    profile_response_json = profile_response.json()
    uid = profile_response_json.get("login", None)

    try:
        # 전달받은 아이디로 등록된 유저가 있는지 탐색
        user = User.objects.get(uid=uid)

        # FK로 연결되어 있는 socialaccount 테이블에서 해당 아이디의 유저가 있는지 확인
        social_user = SocialAccount.objects.get(user=user)

        # 있는데 구글계정이 아니어도 에러
        if social_user.provider != 'fourtytwo':
            return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)

        # 이미 제대로 가입된 유저 => 로그인 & 해당 우저의 jwt 발급
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(f"http://127.0.0.1:8000/users/42/login/finish/", data=data)
        accept_status = accept.status_code

        # 뭔가 중간에 문제가 생기면 에러
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)

        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(accept_json)

    except User.DoesNotExist:
        # 전달받은 아이디로 기존에 가입된 유저가 아예 없으면 => 새로 회원가입 & 해당 유저의 jwt 발급
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(f"http://127.0.0.1:8000/users/42/login/finish/", data=data)
        accept_status = accept.status_code

        # 뭔가 중간에 문제가 생기면 에러
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)

        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(accept_json)

    except SocialAccount.DoesNotExist:
        # User는 있는데 SocialAccount가 없을 때
        return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)


class FourtytwoLoginView(SocialLoginView):
    adapter_class = FourtytwoOAuth2Adapter
    callback_url = FOURTYTWO_CALLBACK_URI
    client_class = OAuth2Client


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
