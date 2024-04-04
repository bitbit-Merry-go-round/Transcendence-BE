import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

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

from game.models import Game

game = Game(player_one="hyecheon", player_two="yham")
game.save()