from django.urls import path

from . import views
from .views import UserCreationAPI, UserDetailAPI

app_name = 'users'

urlpatterns = [
    # /users/hello
    path('hello/', views.HelloAPI),

    path('create/', UserCreationAPI.as_view()),
    path('<pk>/', UserDetailAPI.as_view()),
]
