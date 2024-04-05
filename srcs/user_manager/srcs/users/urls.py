from django.urls import path

from .views import (
    MyProfileAPIView,
    MyFriendAPIView,
    FriendDeleteAPIView,
    UserSearchAPIView,
    UserProfileAPIView,
)

app_name = 'users'

urlpatterns = [
    path('me/profile/', MyProfileAPIView.as_view()),
    path('me/friends/', MyFriendAPIView.as_view()),
    path('me/friends/<str:to_user>/', FriendDeleteAPIView.as_view()),

    path('', UserSearchAPIView.as_view()),
    path('<str:username>/profile/', UserProfileAPIView.as_view()),
]
