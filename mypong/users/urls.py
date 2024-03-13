from django.urls import path, include

from . import views

app_name = 'users'

urlpatterns = [
    # /users/hello
    path('hello/', views.HelloAPI),

    path('<pk>/', include('user_profile.urls')),
]
