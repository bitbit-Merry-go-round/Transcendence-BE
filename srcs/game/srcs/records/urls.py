from django.urls import path

from .views import (
    OneOnOneGameAPIView,
)

app_name = 'records'

urlpatterns = [
    path('<str:username>/1v1s/', OneOnOneGameAPIView.as_view()),
]
