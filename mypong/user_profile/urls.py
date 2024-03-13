from django.urls import path

from .views import UserDetailAPI

app_name = 'user_profile'

urlpatterns = [
    path('profile/', UserDetailAPI.as_view()),
]
