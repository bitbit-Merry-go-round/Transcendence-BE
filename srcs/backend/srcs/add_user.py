import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

import django

import environ

env = environ.Env()
environ.Env.read_env()

django.setup()

from users.models import User

user = User(username="hyecheon", email='hyecheon@test.com')
user.save()
