from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    UserProfileAPIView,
    FriendListAPIView,
    FriendDeleteAPIView,
    UserSearchAPIView,
    fourtytwo_callback,
    MyProfileAPIView,
)

app_name = 'users'

urlpatterns = [
    path('42/callback/', fourtytwo_callback, name='42_callback'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', UserSearchAPIView.as_view()),
    path('me/profile/', MyProfileAPIView.as_view()),
    path('<str:username>/profile/', UserProfileAPIView.as_view()),
    path('<str:from_user>/friends/', FriendListAPIView.as_view()),
    path('<str:from_user>/friends/<str:to_user>/', FriendDeleteAPIView.as_view()),
]
