from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from .serializers import UserLoginSerializer


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return False;


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        return True

    def save_user(self, request, sociallogin, form=None):
        serializer = UserLoginSerializer(data=request.POST)
        serializer.is_valid()

        user = super().save_user(request, sociallogin, form)
        return user
