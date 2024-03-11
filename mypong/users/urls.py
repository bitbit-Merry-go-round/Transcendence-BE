from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    # /users/hello
    path('hello/', views.HelloAPI),
]
