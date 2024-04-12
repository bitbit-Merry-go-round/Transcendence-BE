from django.contrib import admin
from django.urls import path, include
from .views import fourtytwo_callback, OtpValidationAPIView, LogoutAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('42/callback/', fourtytwo_callback, name='42-callback'),
    path('validate-otp/', OtpValidationAPIView.as_view(), name='validate-otp'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('users/', include('users.urls')),
    path('game/', include('game.urls')),
]
