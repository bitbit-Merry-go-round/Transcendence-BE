import re

import requests
import jwt
import environ
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView

env = environ.Env()
environ.Env.read_env()
GAME_CONTAINER_HOST_NAME = "game"


class RouteGameView(APIView):
    permission_classes = [AllowAny]

    # TODO: replace with below
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    def get(self, request):
        token = request.headers.get("Authorization")
        if token is None:
            return JsonResponse({
                "detail": "invalid access token"
            }, status=status.HTTP_401_UNAUTHORIZED)

        bearer, _, token = token.partition(' ')
        payload = jwt.decode(jwt=token, key=env("SECRET_KEY"), algorithms=['HS256'])
        username = payload.get("user_id")

        game_scheme = request.scheme
        game_path = request.path
        game_port = env("GAME_PORT")

        if game_path == "/game/me/1v1s/":
            game_path = "/game/" + username + "/1v1s/"
        if game_path == "/game/me/tournaments/":
            game_path = "/game/" + username + "/tournaments/"

        game_url = f"{game_scheme}://{GAME_CONTAINER_HOST_NAME}:{game_port}{game_path}"
        query = request.META.get("QUERY_STRING")

        if query != "":
            game_url = game_url + f"?{query}"

        response = requests.get(
            game_url,
            headers={"Authorization": f"Bearer {token}"}
        )

        return HttpResponse(
            content=response.content,
            status=response.status_code,
            headers=response.headers
        )

    def post(self, request):
        token = request.headers.get("Authorization")
        if token is None:
            return JsonResponse({
                "detail": "invalid access token"
            }, status=status.HTTP_401_UNAUTHORIZED)

        bearer, _, token = token.partition(' ')
        payload = jwt.decode(jwt=token, key=env("SECRET_KEY"), algorithms=['HS256'])
        username = payload.get("user_id")

        game_scheme = request.scheme
        game_path = request.path
        game_port = env("GAME_PORT")

        # TODO : me가 아닌 경우 예외처리
        if game_path == "/game/me/1v1s/":
            game_path = "/game/" + username + "/1v1s/"
        elif game_path == "/game/me/tournaments/":
            game_path = "/game/" + username + "/tournaments/"

        game_url = f"{game_scheme}://{GAME_CONTAINER_HOST_NAME}:{game_port}{game_path}"
        content_type = request.headers.get("Content-Type")

        response = requests.post(
            game_url,
            data=request.body,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": content_type
            }
        )

        return HttpResponse(
            content=response.content,
            status=response.status_code,
            headers=response.headers
        )

    http_method_names = ['get', 'post', 'options']
