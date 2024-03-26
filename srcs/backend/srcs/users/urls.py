from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    UserProfileAPIView,
    FriendListAPI,
    FriendDeleteAPI,
    oauth_login,
    oauth_callback,
    OAuthLoginView,
)

app_name = 'users'

urlpatterns = [
    path('42/login/', oauth_login, name='42_login'),
    path('42/callback/', oauth_callback, name='42_callback'),
    path('42/login/finish/', OAuthLoginView.as_view(), name='42_login_todjango'),

    path("refresh/", TokenRefreshView.as_view()),

    path('<pk>/profile/', UserProfileAPIView.as_view()),
    path('<str:from_user>/friends/', FriendListAPI.as_view()),
    path('<str:from_user>/friends/<str:to_user>/', FriendDeleteAPI.as_view()),
]
