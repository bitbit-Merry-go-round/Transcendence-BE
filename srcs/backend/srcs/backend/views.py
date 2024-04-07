from json import JSONDecodeError

import requests
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


FOURTYTWO_CALLBACK_URI = 'http%3A%2F%2F127.0.0.1%3A8080%2Flogin'

def fourtytwo_callback(request):
    client_id = settings.FOURTYTWO_CLIENT_ID
    client_secret = settings.FOURTYTWO_CLIENT_SECRET
    code = request.GET.get("code")

    token_response = requests.post(
        f"https://api.intra.42.fr/oauth/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={code}&redirect_uri={FOURTYTWO_CALLBACK_URI}")
    token_response_json = token_response.json()

    error = token_response_json.get("error", None)
    if error is not None:
        raise JSONDecodeError(error)

    access_token = token_response_json.get("access_token")

    profile_response = requests.get(
        "https://api.intra.42.fr/v2/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response_status = profile_response.status_code

    if response_status != 200:
        return JsonResponse({
            'message': 'Bad Request'
        }, status=response_status)

    profile_response_json = profile_response.json()
    username = profile_response_json.get("login")

    try:
        user = User.objects.get(username=username)
        token = RefreshToken.for_user(user)
        refresh = str(token)
        access = str(token.access_token)

        return JsonResponse({
            'access': access,
            'refresh': refresh,
        }, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        new_user = User(username=username)
        new_user.set_unusable_password()
        new_user.save()
        token = RefreshToken.for_user(new_user)
        refresh = str(token)
        access = str(token.access_token)

        return JsonResponse({
            'access': access,
            'refresh': refresh,
        }, status=status.HTTP_201_CREATED)


