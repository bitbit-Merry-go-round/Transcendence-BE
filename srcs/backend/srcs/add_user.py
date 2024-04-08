import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

import django

import environ

env = environ.Env()
environ.Env.read_env()

django.setup()

from users.models import User

username = "hyecheon"
user = User(username=f"{username}", email=f"{username}@student.42seoul.kr")
user.save()
