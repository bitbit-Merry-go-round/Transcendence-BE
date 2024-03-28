from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

from .provider import FourtytwoProvider

urlpatterns = default_urlpatterns(FourtytwoProvider)
