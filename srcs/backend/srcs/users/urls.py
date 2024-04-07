from django.urls import path

from .views import RouteUserView

app_name = 'users'

urlpatterns = [
    path('', RouteUserView.as_view()),
]
