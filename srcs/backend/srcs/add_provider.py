import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

import django

import environ

env = environ.Env()
environ.Env.read_env()

django.setup()

from allauth.socialaccount.models import SocialApp

if len(SocialApp.objects.filter(provider='fourtytwo')) == 0:
    app = SocialApp(
        provider='fourtytwo',
        name='42-login',
        client_id=env("FOURTYTWO_CLIENT_ID"),
        secret=env("FOURTYTWO_CLIENT_SECRET"),
        provider_id='fourtytwo'
    )
    app.save()
