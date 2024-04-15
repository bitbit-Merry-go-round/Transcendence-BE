import json

import requests
import environ
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView

env = environ.Env()
environ.Env.read_env()
GAME_CONTAINER_HOST_NAME = "game"
USER_MANAGER_HOST_NAME = "user-manager"


class RouteGameView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        token = request.headers.get("Authorization")
        if token is None:
            return JsonResponse({
                "detail": "invalid access token"
            }, status=status.HTTP_401_UNAUTHORIZED)

        game_scheme = request.scheme
        game_path = request.path
        game_port = env("GAME_PORT")

        game_url = f"{game_scheme}://{GAME_CONTAINER_HOST_NAME}:{game_port}{game_path}"
        query = request.META.get("QUERY_STRING")

        if query != "":
            game_url = game_url + f"?{query}"

        bearer, _, token = token.partition(' ')
        response = requests.get(
            game_url,
            headers={"Authorization": f"Bearer {token}"}, 
            verify=False
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

        game_scheme = request.scheme
        game_path = request.path
        game_port = env("GAME_PORT")

        game_url = f"{game_scheme}://{GAME_CONTAINER_HOST_NAME}:{game_port}{game_path}"
        content_type = request.headers.get("Content-Type")

        bearer, _, token = token.partition(' ')
        response = requests.post(
            game_url,
            data=request.body,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": content_type
            }, verify=False
        )

        if response.status_code == 201 and game_path == "/api/game/me/1v1s/":
            user_manager_scheme = request.scheme
            user_manager_port = env("USER_MANAGER_PORT")
            user_manager_path = "/api/users/me/profile/"

            user_profile_url = f"{user_manager_scheme}://{USER_MANAGER_HOST_NAME}:{user_manager_port}{user_manager_path}"

            my_score = json.loads(request.body)["player_one_score"]
            if my_score == 3:
                data = {"wins": 1}
            else:
                data = {"loses": 1}
            json_data = json.dumps(data)

            token = request.headers.get("Authorization")
            bearer, _, token = token.partition(' ')
            user_profile_response = requests.patch(
                user_profile_url,
                data=json_data,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }, verify=False
            )

        return HttpResponse(
            content=response.content,
            status=response.status_code,
            headers=response.headers
        )

    http_method_names = ['get', 'post', 'options']
