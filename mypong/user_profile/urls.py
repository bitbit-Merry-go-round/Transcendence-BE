from django.urls import path

from .views import UserProfileAPI

app_name = 'user_profile'

urlpatterns = [
    path('profile/', UserProfileAPI.as_view()),
]
