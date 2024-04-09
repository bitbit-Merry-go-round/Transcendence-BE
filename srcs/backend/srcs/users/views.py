import requests
import jwt
import environ
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView

env = environ.Env()
environ.Env.read_env()
USER_MANAGER_HOST_NAME = "user-manager"


class RouteToUserManagerAPIView(APIView):
    permission_classes = [AllowAny]

    # TODO: replace with below
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    def get(self, request):
        token = request.headers.get("Authorization")
        bearer, _, token = token.partition(' ')
        payload = jwt.decode(jwt=token, key=env("SECRET_KEY"), algorithms=['HS256'])
        username = payload.get("user_id")

        query = request.META.get("QUERY_STRING")

        user_manager_scheme = request.scheme
        user_manager_port = env("USER_MANAGER_PORT")
        user_manager_path = request.path

        if "me" in user_manager_path:
            user_manager_path = user_manager_path.replace("me", username)

        user_manager_url = f"{user_manager_scheme}://{USER_MANAGER_HOST_NAME}:{user_manager_port}{user_manager_path}"

        if query != "":
            user_manager_url = user_manager_url + f"?{query}"

        response = requests.get(
            user_manager_url,
            params=self.request.method,
            headers={"Authorization": f"Bearer {token}"}
        )

        return HttpResponse(
            content=response.content,
            status=response.status_code,
            headers=response.headers
        )

    def patch(self, request):
        token = request.headers.get("Authorization")
        bearer, _, token = token.partition(' ')
        payload = jwt.decode(jwt=token, key=env("SECRET_KEY"), algorithms=['HS256'])
        username = payload.get("user_id")

        user_manager_scheme = request.scheme
        user_manager_port = env("USER_MANAGER_PORT")
        user_manager_path = request.path

        if "me" in user_manager_path:
            user_manager_path = user_manager_path.replace("me", username)

        user_manager_url = f"{user_manager_scheme}://{USER_MANAGER_HOST_NAME}:{user_manager_port}{user_manager_path}"
        content_type = request.headers.get("Content-Type")

        response = requests.patch(
            user_manager_url,
            params=self.request.method,
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

    def post(self, request):
        token = request.headers.get("Authorization")
        bearer, _, token = token.partition(' ')
        payload = jwt.decode(jwt=token, key=env("SECRET_KEY"), algorithms=['HS256'])
        username = payload.get("user_id")

        user_manager_scheme = request.scheme
        user_manager_port = env("USER_MANAGER_PORT")
        user_manager_path = request.path

        if "me" in user_manager_path:
            user_manager_path = user_manager_path.replace("me", username)

        user_manager_url = f"{user_manager_scheme}://{USER_MANAGER_HOST_NAME}:{user_manager_port}{user_manager_path}"
        content_type = request.headers.get("Content-Type")

        response = requests.post(
            user_manager_url,
            params=self.request.method,
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

    def delete(self, request):
        token = request.headers.get("Authorization")
        bearer, _, token = token.partition(' ')
        payload = jwt.decode(jwt=token, key=env("SECRET_KEY"), algorithms=['HS256'])
        username = payload.get("user_id")

        user_manager_scheme = request.scheme
        user_manager_port = env("USER_MANAGER_PORT")
        user_manager_path = request.path

        if "me" in user_manager_path:
            user_manager_path = user_manager_path.replace("me", username)

        user_manager_url = f"{user_manager_scheme}://{USER_MANAGER_HOST_NAME}:{user_manager_port}{user_manager_path}"

        response = requests.delete(
            user_manager_url,
            params=self.request.method,
            headers={"Authorization": f"Bearer {token}"}
        )

        return HttpResponse(
            content=response.content,
            status=response.status_code,
            headers=response.headers
        )

    http_method_names = ['get', 'post', 'patch', 'delete', 'options']
