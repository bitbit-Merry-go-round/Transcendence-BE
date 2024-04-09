from django.urls import re_path

from .views import RouteUserView

app_name = 'users'

urlpatterns = [
    re_path(r'.*', RouteUserView.as_view()),
]
