from django.urls import path, include

from . import views
from .views import UserCreationAPI, UserProfileAPI

app_name = 'users'

urlpatterns = [
    # /users/hello
    path('hello/', views.HelloAPI),

    path('create/', UserCreationAPI.as_view()),
    path('<pk>/profile/', UserProfileAPI.as_view()),
]
