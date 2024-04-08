import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "user_manager.settings")

import django

import environ

env = environ.Env()
environ.Env.read_env()

django.setup()

from users.models import User

user = User(username="hyecheon")
user.save()

user = User(username="yham")
user.save()

user = User(username="test1")
user.save()

user = User(username="test2")
user.save()

user = User(username="test3")
user.save()

user = User(username="test4")
user.save()
