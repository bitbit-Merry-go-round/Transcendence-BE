import os
from datetime import datetime

from django.utils.timezone import make_aware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "game.settings")

import django

import environ

env = environ.Env()
environ.Env.read_env()

django.setup()

from records.models import Game

time_str = "2024/03/13 16:38:28"
time = datetime.strptime(time_str, "%Y/%m/%d %H:%M:%S")
aware_datetime = make_aware(time)
game = Game(
    player_one="yham",
    player_two="guest",
    player_one_score=3,
    player_two_score=2,
    time=aware_datetime,
    type="1v1"
)
game.save()

time_str = "2024/04/10 20:25:40"
time = datetime.strptime(time_str, "%Y/%m/%d %H:%M:%S")
aware_datetime = make_aware(time)
game = Game(
    player_one="yham",
    player_two="guest",
    player_one_score=1,
    player_two_score=3,
    time=aware_datetime,
    type="1v1"
)
game.save()
