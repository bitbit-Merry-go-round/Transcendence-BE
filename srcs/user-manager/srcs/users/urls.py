from django.urls import path

from .views import (
    MyFriendAPIView,
    FriendDeleteAPIView,
    UserSearchAPIView,
    UserProfileAPIView,
    UserCreationAPIView,
)

app_name = 'users'

urlpatterns = [
    path('<str:username>/profile/', UserProfileAPIView.as_view()),
    path('<str:username>/friends/', MyFriendAPIView.as_view()),
    path('<str:from_user>/friends/<str:to_user>/', FriendDeleteAPIView.as_view()),
    path('create/', UserCreationAPIView.as_view()),

    path('', UserSearchAPIView.as_view()),
]
