import requests
import jwt
import environ
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView

env = environ.Env()
environ.Env.read_env()
USER_CONTAINER_HOST_NAME = "user-manager"
class RouteUserView(APIView):
    permission_classes = [AllowAny]
    # TODO: replace with below
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    def get(self, request):
        # TODO: url에 me 들어간 경우 username으로 치환하여 요청
        # TODO: 유효한 url로 접근해야 함.
        token = request.headers.get("Authorization")
        bearer, _, token = token.partition(' ')
        payload = jwt.decode(jwt=token, key=env("SECRET_KEY"), algorithms=['HS256'])
        query = request.META.get("QUERY_STRING")
        user_manager_path = request.path
        if "me" in request.path:
            user_manager_path = user_manager_path.replace("me", payload.get("user_id"))
        if query is not "":
            url = f"{request.scheme}://{USER_CONTAINER_HOST_NAME}:{env("USER_MANAGER_PORT")}{user_manager_path}?{query}"
        else:
            url = f"{request.scheme}://{USER_CONTAINER_HOST_NAME}:{env("USER_MANAGER_PORT")}{user_manager_path}"

        response = requests.get(
            url,
            params=self.request.method,
            headers={"Authorization": f"Bearer {token}"}
        )
        headers = response.headers

        return HttpResponse(
            content=response.content,
            status=response.status_code,
            headers=headers
        )

    def patch(self, request):
        token = request.headers.get("Authorization")
        bearer, _, token = token.partition(' ')
        payload = jwt.decode(jwt=token, key=env("SECRET_KEY"), algorithms=['HS256'])
        if "me" in request.path:
            user_manager_path = request.path.replace("me", payload.get("user_id"))
        url = f"{request.scheme}://{USER_CONTAINER_HOST_NAME}:{env("USER_MANAGER_PORT")}{user_manager_path}"

        content_type = request.headers.get("Content-Type")
        response = requests.patch(
            url,
            params=self.request.method,
            data=request.body,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": content_type
            }
        )
        headers = response.headers

        return HttpResponse(
            content=response.content,
            status=response.status_code,
            headers=headers
        )
    
    def post(self, request):
        token = request.headers.get("Authorization")
        bearer, _, token = token.partition(' ')
        payload = jwt.decode(jwt=token, key=env("SECRET_KEY"), algorithms=['HS256'])
        if "me" in request.path:
            user_manager_path = request.path.replace("me", payload.get("user_id"))
        url = f"{request.scheme}://{USER_CONTAINER_HOST_NAME}:{env("USER_MANAGER_PORT")}{user_manager_path}"

        content_type = request.headers.get("Content-Type")
        response = requests.post(
            url,
            params=self.request.method,
            data=request.body,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": content_type
            }
        )
        headers = response.headers

        return HttpResponse(
            content=response.content,
            status=response.status_code,
            headers=headers
        )

    def delete(self, request):
        token = request.headers.get("Authorization")
        bearer, _, token = token.partition(' ')
        payload = jwt.decode(jwt=token, key=env("SECRET_KEY"), algorithms=['HS256'])
        user_manager_path = request.path
        if "me" in request.path:
            user_manager_path = user_manager_path.replace("me", payload.get("user_id"))
        url = f"{request.scheme}://{USER_CONTAINER_HOST_NAME}:{env("USER_MANAGER_PORT")}{user_manager_path}"

        response = requests.delete(
            url,
            params=self.request.method,
            headers={"Authorization": f"Bearer {token}"}
        )
        headers = response.headers

        return HttpResponse(
            content=response.content,
            status=response.status_code,
            headers=headers
        )

    http_method_names = ['get', 'post', 'patch', 'delete', 'options']
    