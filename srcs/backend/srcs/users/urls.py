from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    UserProfileAPIView,
    FriendListAPI,
    FriendDeleteAPI,
    UserRegisterAPIView,
    UserLoginAPIView
)

app_name = 'users'

urlpatterns = [
    path('register/', UserRegisterAPIView.as_view()),
    path('login/', UserLoginAPIView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),

    path('<pk>/profile/', UserProfileAPIView.as_view()),
    path('<str:from_user>/friends/', FriendListAPI.as_view()),
    path('<str:from_user>/friends/<str:to_user>/', FriendDeleteAPI.as_view()),
]
