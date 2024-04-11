from django.urls import path

from .views import (
    OneOnOneGameAPIView,
    TournamentAPIView,
)

app_name = 'records'

urlpatterns = [
    path('<str:username>/1v1s/', OneOnOneGameAPIView.as_view()),
    path('<str:username>/tournaments/', TournamentAPIView.as_view()),
]
