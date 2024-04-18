import requests
import environ
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView

env = environ.Env()
environ.Env.read_env()
USER_MANAGER_HOST_NAME = "user-manager"


class RouteToUserManagerAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        token = request.headers.get("Authorization")
        if token is None:
            return JsonResponse({
                "detail": "invalid access token"
            }, status=status.HTTP_401_UNAUTHORIZED)

        user_manager_scheme = request.scheme
        user_manager_port = env("USER_MANAGER_PORT")
        user_manager_path = request.path

        user_manager_url = f"{user_manager_scheme}://{USER_MANAGER_HOST_NAME}:{user_manager_port}{user_manager_path}"

        query = request.META.get("QUERY_STRING")
        if query != "":
            user_manager_url = user_manager_url + f"?{query}"

        bearer, _, token = token.partition(' ')
        response = requests.get(
            user_manager_url,
            headers={"Authorization": f"Bearer {token}"}, 
            verify=False
        )

        return HttpResponse(
            content=response.content,
            status=response.status_code,
            headers=response.headers
        )

    def patch(self, request):
        token = request.headers.get("Authorization")
        if token is None:
            return JsonResponse({
                "detail": "invalid access token"
            }, status=status.HTTP_401_UNAUTHORIZED)

        user_manager_scheme = request.scheme
        user_manager_port = env("USER_MANAGER_PORT")
        user_manager_path = request.path

        user_manager_url = f"{user_manager_scheme}://{USER_MANAGER_HOST_NAME}:{user_manager_port}{user_manager_path}"
        content_type = request.headers.get("Content-Type")

        bearer, _, token = token.partition(' ')
        response = requests.patch(
            user_manager_url,
            data=request.body,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": content_type
            }, verify=False
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

        user_manager_scheme = request.scheme
        user_manager_port = env("USER_MANAGER_PORT")
        user_manager_path = request.path

        user_manager_url = f"{user_manager_scheme}://{USER_MANAGER_HOST_NAME}:{user_manager_port}{user_manager_path}"
        content_type = request.headers.get("Content-Type")

        bearer, _, token = token.partition(' ')
        response = requests.post(
            user_manager_url,
            data=request.body,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": content_type
            }, verify=False
        )

        return HttpResponse(
            content=response.content,
            status=response.status_code,
            headers=response.headers
        )

    def delete(self, request):
        token = request.headers.get("Authorization")
        if token is None:
            return JsonResponse({
                "detail": "invalid access token"
            }, status=status.HTTP_401_UNAUTHORIZED)

        user_manager_scheme = request.scheme
        user_manager_port = env("USER_MANAGER_PORT")
        user_manager_path = request.path

        user_manager_url = f"{user_manager_scheme}://{USER_MANAGER_HOST_NAME}:{user_manager_port}{user_manager_path}"

        bearer, _, token = token.partition(' ')
        response = requests.delete(
            user_manager_url,
            headers={"Authorization": f"Bearer {token}"}, verify=False
        )

        return HttpResponse(
            content=response.content,
            status=response.status_code,
            headers=response.headers
        )

    http_method_names = ['get', 'patch', 'post', 'delete', 'options']
