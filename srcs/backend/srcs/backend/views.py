from json import JSONDecodeError

import requests
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenBlacklistView
from users.models import User
from users.utils import generate_otp, send_otp_email


# Login with Email OTP
class ValidateOTP(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username', '')
        otp = request.data.get('otp', '')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User email does not match.'}, status=status.HTTP_404_NOT_FOUND)

        if user.otp == otp:
            user.otp = None
            user.email_verified = True
            user.save()
            response = requests.post(f"http://user-manager:8001/users/create/", json={
                "username": user.username,
                "email": user.email
            })

            token = RefreshToken.for_user(user)
            refresh = str(token)
            access = str(token.access_token)

            return JsonResponse({
                'access': access,
                'refresh': refresh,
            }, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)


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
    email = profile_response_json.get("email")

    try:
        user = User.objects.get(username=username)
        otp = generate_otp()
        user.otp = otp
        user.save()
        send_otp_email(user.email, otp)

        return JsonResponse({"username": username}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        new_user = User(username=username, email=email)
        new_user.set_unusable_password()
        new_user.save()
        otp = generate_otp()
        new_user.otp = otp
        new_user.save()
        send_otp_email(new_user.email, otp)

        return JsonResponse({"username": username}, status=status.HTTP_201_CREATED)


class LogoutAPIView(TokenBlacklistView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        refresh = request.data["refresh"]
        data = {"refresh": str(refresh)}
        serializer = self.get_serializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response = Response({"detail": "token blacklisted"}, status=status.HTTP_200_OK)

        return response

    http_method_names = ['post', 'options']
