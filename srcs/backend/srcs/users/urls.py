from django.urls import path

from . import views
from .views import UserCreationAPI, UserProfileAPI, FriendListAPI, FriendDeleteAPI

app_name = 'users'

urlpatterns = [
    # /users/hello
    path('hello/', views.HelloAPI),

    path('create/', UserCreationAPI.as_view()),
    path('<pk>/profile/', UserProfileAPI.as_view()),
    path('<str:from_user>/friends/', FriendListAPI.as_view()),
    path('<str:from_user>/friends/<str:to_user>/', FriendDeleteAPI.as_view()),
]
