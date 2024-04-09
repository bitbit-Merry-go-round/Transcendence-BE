from django.urls import re_path

from .views import RouteToUserManagerAPIView

app_name = 'users'

urlpatterns = [
    re_path(r'.*', RouteToUserManagerAPIView.as_view()),
]
