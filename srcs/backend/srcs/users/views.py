import requests
import environ
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from .utils import get_container_ip

env = environ.Env()
environ.Env.read_env()
USER_CONTAINER_HOST_NAME = "user_manager"
class RouteUserView(APIView):
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]
    def get(self, request):
        # 컨테이너의 IP 주소 얻기
        container_ip = get_container_ip(USER_CONTAINER_HOST_NAME)
        print(f"Container IP: {container_ip}")
        print(f"Container IP: {container_ip}")
        print(f"Container IP: {container_ip}")
        # TODO: url에 me 들어간 경우 username으로 치환하여 요청
        # TODO: 유효한 url로 접근해야 함.
        url = f"{request.scheme}://{USER_CONTAINER_HOST_NAME}:{env("USER_MANAGER_PORT")}{request.path}"
        print(url)
        print(url)
        print(url)
        print(url)
        print(url)
        
        response = requests.get(url, params=request.GET)
        headers = response.headers

        return HttpResponse(
            content=response.content,
            status=response.status_code,
            content_type=headers['Content-Type']
        )

    # def post(self, request):
    #     url = f"{request.scheme}://{request.get_host()}:{env("USER_MANAGER_PORT")}"
    #     # url에 me 들어간 경우 username으로 치환하여 요청
        
    #     # 클라이언트로부터 받은 메소드와 데이터를 그대로 전달.
    #     response = requests.get(url, headers=headers, params=request.POST)
    #     # response = requests.post(url, headers=headers, data=request.POST)

    #     return Response(
    #         content=response.content,
    #         status=response.status_code,
    #         content_type=headers['Content-Type']
    #     )
    
    # def patch(self, request):
    #     url = f"{request.scheme}://{request.get_host()}:{env("USER_MANAGER_PORT")}"
    #     # url에 me 들어간 경우 username으로 치환하여 요청
        
    #     # 클라이언트로부터 받은 메소드와 데이터를 그대로 전달.
    #     response = requests.get(url, headers=headers, params=request.PATCH)
    #     # response = requests.post(url, headers=headers, data=request.POST)

    #     return Response(
    #         content=response.content,
    #         status=response.status_code,
    #         content_type=headers['Content-Type']
    #     )
    
    # def delete(self, request):
    #     url = f"{request.scheme}://{request.get_host()}:{env("USER_MANAGER_PORT")}"
    #     # url에 me 들어간 경우 username으로 치환하여 요청
        
    #     # 클라이언트로부터 받은 메소드와 데이터를 그대로 전달.
    #     response = requests.get(url, headers=headers, params=request.DELETE)
    #     # response = requests.post(url, headers=headers, data=request.POST)

    #     return Response(
    #         content=response.content,
    #         status=response.status_code,
    #         content_type=headers['Content-Type']
    #     )    
