from django.urls import path

from .views import (
    MyOneOnOneGameAPIView,
    MyTournamentAPIView,
    UserOneOnOneGameAPIView,
    UserTournamentAPIView,
    TournamentDetailAPIView,
)

app_name = 'records'

urlpatterns = [
    path('me/1v1s/', MyOneOnOneGameAPIView.as_view()),
    path('me/tournaments/', MyTournamentAPIView.as_view()),
    path('<str:username>/1v1s/', UserOneOnOneGameAPIView.as_view()),
    path('<str:username>/tournaments/', UserTournamentAPIView.as_view()),
    path('tournaments/<int:tournament_id>/', TournamentDetailAPIView.as_view()),
]
