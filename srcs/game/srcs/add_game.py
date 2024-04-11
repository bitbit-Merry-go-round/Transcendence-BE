import os
from datetime import datetime

from django.utils.timezone import make_aware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "game.settings")

import django

import environ

env = environ.Env()
environ.Env.read_env()

django.setup()

from records.models import Game, Tournament

# ====================================================================

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

time_str = "2024/04/11 14:47:40"
time = datetime.strptime(time_str, "%Y/%m/%d %H:%M:%S")
aware_datetime = make_aware(time)
game = Game(
    player_one="hyecheon",
    player_two="guest",
    player_one_score=3,
    player_two_score=1,
    time=aware_datetime,
    type="1v1"
)
game.save()

# ====================================================================

time_str = "2024/04/11 14:13:00"
time = datetime.strptime(time_str, "%Y/%m/%d %H:%M:%S")
aware_datetime = make_aware(time)
game1 = Game(
    player_one="hyecheon",
    player_two="jeseo",
    player_one_score=3,
    player_two_score=2,
    time=aware_datetime,
    type="tournament"
)
game1.save()

time_str = "2024/04/11 14:15:00"
time = datetime.strptime(time_str, "%Y/%m/%d %H:%M:%S")
aware_datetime = make_aware(time)
game2 = Game(
    player_one="eunjiko",
    player_two="heshin",
    player_one_score=1,
    player_two_score=3,
    time=aware_datetime,
    type="tournament"
)
game2.save()

time_str = "2024/04/11 14:17:00"
time = datetime.strptime(time_str, "%Y/%m/%d %H:%M:%S")
aware_datetime = make_aware(time)
game3 = Game(
    player_one="hyecheon",
    player_two="heshin",
    player_one_score=2,
    player_two_score=3,
    time=aware_datetime,
    type="tournament"
)
game3.save()

tournament = Tournament(
    game_one=game1,
    game_two=game2,
    game_three=game3,
    username="yham"
)
tournament.save()

# ====================================================================

time_str = "2024/03/11 14:13:00"
time = datetime.strptime(time_str, "%Y/%m/%d %H:%M:%S")
aware_datetime = make_aware(time)
game4 = Game(
    player_one="muji",
    player_two="chunsik",
    player_one_score=1,
    player_two_score=3,
    time=aware_datetime,
    type="tournament"
)
game4.save()

time_str = "2024/03/11 14:15:00"
time = datetime.strptime(time_str, "%Y/%m/%d %H:%M:%S")
aware_datetime = make_aware(time)
game5 = Game(
    player_one="ryan",
    player_two="apeach",
    player_one_score=3,
    player_two_score=2,
    time=aware_datetime,
    type="tournament"
)
game5.save()

time_str = "2024/03/11 14:17:00"
time = datetime.strptime(time_str, "%Y/%m/%d %H:%M:%S")
aware_datetime = make_aware(time)
game6 = Game(
    player_one="chunsik",
    player_two="ryan",
    player_one_score=3,
    player_two_score=1,
    time=aware_datetime,
    type="tournament"
)
game6.save()

tournament = Tournament(
    game_one=game4,
    game_two=game5,
    game_three=game6,
    username="yham"
)
tournament.save()
