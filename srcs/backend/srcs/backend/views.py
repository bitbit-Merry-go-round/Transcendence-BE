import json
import environ
import requests
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenBlacklistView
from users.models import User
from users.utils import generate_otp, send_otp_email

env = environ.Env()
environ.Env.read_env()
USER_MANAGER_HOST_NAME = "user-manager"


class OtpValidationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username', '')
        otp = request.data.get('otp', '')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({
                'detail': 'user email does not match'
            }, status=status.HTTP_404_NOT_FOUND)

        if user.otp == otp:
            user.otp = None
            user.email_verified = True
            user.save()
            response = requests.post(
                f"https://user-manager:8001/api/users/create/",
                json={
                    "username": user.username,
                    "email": user.email
                }, 
                verify=False
            )

            token = RefreshToken.for_user(user)
            refresh = str(token)
            access = str(token.access_token)

            user_manager_scheme = request.scheme
            user_manager_port = env("USER_MANAGER_PORT")
            user_manager_path = "/api/users/me/profile/"

            user_profile_url = f"{user_manager_scheme}://{USER_MANAGER_HOST_NAME}:{user_manager_port}{user_manager_path}"

            data = {"status": "ONLINE"}
            json_data = json.dumps(data)

            response = requests.patch(
                user_profile_url,
                data=json_data,
                headers={
                    "Authorization": f"Bearer {access}",
                    "Content-Type": "application/json"
                }, verify=False
            )

            return JsonResponse({
                'access': access,
                'refresh': refresh
            }, status=status.HTTP_200_OK)

        else:
            return JsonResponse({
                'detail': 'invalid OTP'
            }, status=status.HTTP_400_BAD_REQUEST)




def fourtytwo_callback(request):
    client_id = settings.FOURTYTWO_CLIENT_ID
    client_secret = settings.FOURTYTWO_CLIENT_SECRET
    redirect_uri = settings.FOURTYTWO_REDIRECT_URI
    code = request.GET.get("code")

    token_response = requests.post(
        f"https://api.intra.42.fr/oauth/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={code}&redirect_uri={redirect_uri}"
    , verify=False)
    response_status = token_response.status_code
    token_response_json = token_response.json()

    error = token_response_json.get("error", None)
    if error is not None:
        return JsonResponse({
            "detail": error
        }, status=response_status)

    access_token = token_response_json.get("access_token")

    profile_response = requests.get(
        "https://api.intra.42.fr/v2/me",
        headers={"Authorization": f"Bearer {access_token}"}, verify=False
    )
    response_status = profile_response.status_code

    if response_status != 200:
        return JsonResponse({
            "detail": "failed to fetch 42 profile"
        }, status=response_status)

    profile_response_json = profile_response.json()
    username = profile_response_json.get("login")
    email = profile_response_json.get("email")

    try:
        user = User.objects.get(username=username)
        otp = generate_otp()
        user.otp = otp
        user.save()
        send_otp_email(user.email, otp)

        return JsonResponse({
            "username": username
        }, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        new_user = User(username=username, email=email)
        new_user.set_unusable_password()
        new_user.save()
        otp = generate_otp()
        new_user.otp = otp
        new_user.save()
        send_otp_email(new_user.email, otp)

        return JsonResponse({
            "username": username
        }, status=status.HTTP_201_CREATED)


class LogoutAPIView(TokenBlacklistView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            refresh = request.data["refresh"]
        except:
            return JsonResponse({
                "detail": "invalid refresh token"
            }, status=status.HTTP_400_BAD_REQUEST)

        data = {"refresh": str(refresh)}
        serializer = self.get_serializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        user_manager_scheme = request.scheme
        user_manager_port = env("USER_MANAGER_PORT")
        user_manager_path = "/api/users/me/profile/"

        user_profile_url = f"{user_manager_scheme}://{USER_MANAGER_HOST_NAME}:{user_manager_port}{user_manager_path}"

        data = {"status": "OFFLINE"}
        json_data = json.dumps(data)

        token = request.headers.get("Authorization")
        bearer, _, token = token.partition(' ')
        response = requests.patch(
            user_profile_url,
            data=json_data,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }, verify=False
        )

        return JsonResponse({
            "detail": "logout success"
        }, status=status.HTTP_200_OK)

    http_method_names = ['post', 'options']
