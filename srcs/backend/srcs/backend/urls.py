from django.contrib import admin
from django.urls import path, include
from .views import fourtytwo_callback, OtpValidationAPIView, LogoutAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/42/callback/', fourtytwo_callback, name='42-callback'),
    path('api/validate-otp/', OtpValidationAPIView.as_view(), name='validate-otp'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('api/logout/', LogoutAPIView.as_view(), name='logout'),
    path('api/users/', include('users.urls')),
    path('api/game/', include('game.urls')),
]
