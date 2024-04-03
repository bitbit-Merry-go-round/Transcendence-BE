from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    fourtytwo_callback,
    MyProfileAPIView,
    MyFriendAPIView,
    FriendDeleteAPIView,
    UserSearchAPIView,
    UserProfileAPIView,
)

app_name = 'users'

urlpatterns = [
    path('42/callback/', fourtytwo_callback, name='42_callback'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('me/profile/', MyProfileAPIView.as_view()),
    path('me/friends/', MyFriendAPIView.as_view()),
    path('me/friends/<str:to_user>/', FriendDeleteAPIView.as_view()),

    path('', UserSearchAPIView.as_view()),
    path('<str:username>/profile/', UserProfileAPIView.as_view()),
]
