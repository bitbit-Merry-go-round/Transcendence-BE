import requests
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView

class RouteUserView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        url = f"{request.scheme}://{request.get_host()}:{env("USER_MANAGER_PORT")}"
        # url에 me 들어간 경우 username으로 치환하여 요청
        print(url)
        # 클라이언트로부터 받은 메소드와 데이터를 그대로 전달.
        response = requests.get(url, headers=headers, params=request.GET)
        # response = requests.post(url, headers=headers, data=request.POST)

        return Response(
            content=response.content,
            status=response.status_code,
            content_type=response.headers['Content-Type']
        )

    def post(self, request):
        url = f"{request.scheme}://{request.get_host()}:{env("USER_MANAGER_PORT")}"
        # url에 me 들어간 경우 username으로 치환하여 요청
        
        # 클라이언트로부터 받은 메소드와 데이터를 그대로 전달.
        response = requests.get(url, headers=headers, params=request.POST)
        # response = requests.post(url, headers=headers, data=request.POST)

        return Response(
            content=response.content,
            status=response.status_code,
            content_type=response.headers['Content-Type']
        )
    
    def patch(self, request):
        url = f"{request.scheme}://{request.get_host()}:{env("USER_MANAGER_PORT")}"
        # url에 me 들어간 경우 username으로 치환하여 요청
        
        # 클라이언트로부터 받은 메소드와 데이터를 그대로 전달.
        response = requests.get(url, headers=headers, params=request.PATCH)
        # response = requests.post(url, headers=headers, data=request.POST)

        return Response(
            content=response.content,
            status=response.status_code,
            content_type=response.headers['Content-Type']
        )
    
    def delete(self, request):
        url = f"{request.scheme}://{request.get_host()}:{env("USER_MANAGER_PORT")}"
        # url에 me 들어간 경우 username으로 치환하여 요청
        
        # 클라이언트로부터 받은 메소드와 데이터를 그대로 전달.
        response = requests.get(url, headers=headers, params=request.DELETE)
        # response = requests.post(url, headers=headers, data=request.POST)

        return Response(
            content=response.content,
            status=response.status_code,
            content_type=response.headers['Content-Type']
        )    
