from django.urls import re_path

from .views import RouteGameView

app_name = 'users'

urlpatterns = [
    re_path(r'.*', RouteGameView.as_view()),
]
