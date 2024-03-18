from django.urls import path, include

from . import views
from .views import UserCreationAPI

app_name = 'users'

urlpatterns = [
    # /users/hello
    path('hello/', views.HelloAPI),

    path('create/', UserCreationAPI.as_view()),
    path('<pk>/', include('user_profile.urls')),
]
