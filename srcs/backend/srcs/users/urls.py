from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    UserProfileAPIView,
    FriendListAPIView,
    FriendDeleteAPIView,
    UserSearchAPIView,
    fourtytwo_login,
    fourtytwo_callback,
    FourtytwoLoginView,
)

app_name = 'users'

urlpatterns = [
    path('42/login/', fourtytwo_login, name='42_login'),
    path('42/callback/', fourtytwo_callback, name='42_callback'),
    path('42/login/finish/', FourtytwoLoginView.as_view(), name='42_login_to_django'),

    path('', UserSearchAPIView.as_view()),
    path('<pk>/profile/', UserProfileAPIView.as_view()),
    path('<str:from_user>/friends/', FriendListAPIView.as_view()),
    path('<str:from_user>/friends/<str:to_user>/', FriendDeleteAPIView.as_view()),
]
