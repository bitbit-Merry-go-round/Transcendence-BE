from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_username, user_email, user_field
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.utils import valid_email_or_none

from .serializers import UserLoginSerializer


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return False;


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        return True

    def populate_user(self, request, sociallogin, data):
        username = data.get("username")
        email = data.get("email")
        user = sociallogin.user
        user_username(user, username or "")
        user_email(user, valid_email_or_none(email) or "")
        user_field(user, "username", sociallogin.account.uid)
        return user

    def save_user(self, request, sociallogin, form=None):
        serializer = UserLoginSerializer(data=request.POST)
        serializer.is_valid()

        user = super().save_user(request, sociallogin, form)
        return user
