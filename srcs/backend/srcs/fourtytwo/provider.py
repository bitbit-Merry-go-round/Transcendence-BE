from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class FourtytwoAccount(ProviderAccount):
    def get_uid(self):
        return self.account.extra_data.get('login')

    def get_avatar_url(self):
        return self.account.extra_data.get('image_url')

    def to_str(self):
        dflt = super(FourtytwoAccount, self).to_str()
        return self.account.extra_data.get('login', dflt)


class FourtytwoProvider(OAuth2Provider):
    id = 'fourtytwo'
    name = '42'
    account_class = FourtytwoAccount

    def extract_uid(self, data):
        return str(data['login'])

    def extract_common_fields(self, data):
        uid = data.get("login")
        return dict(uid=uid)


providers.registry.register(FourtytwoProvider)
