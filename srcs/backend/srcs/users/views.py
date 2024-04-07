import requests
import environ
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView

env = environ.Env()
environ.Env.read_env()
class RouteUserView(APIView):
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    def get(self, request):
        # TODO: url에 me 들어간 경우 username으로 치환하여 요청
        # TODO: {request.META.get('REMOTE_ADDR')} 이 부분 유효한 녀석으로 변경해야 함.
        url = f"{request.scheme}://{request.META.get('REMOTE_ADDR')}:{env("USER_MANAGER_PORT")}"
        response = requests.get(url, params=request.GET)
        # response = requests.post(url, headers=headers, data=request.POST)

        return Response(
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
