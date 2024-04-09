#!/bin/sh

cat << EOF > ./.env
SECRET_KEY=${SECRET_KEY}

GAME_DB_NAME=${GAME_DB_NAME}
GAME_DB_HOST=${GAME_DB_HOST}
GAME_DB_USER=${GAME_DB_USER}
GAME_DB_PW=${GAME_DB_PW}
GAME_DB_PORT=${GAME_DB_PORT}

GAME_PORT=${GAME_PORT}
EOF

python manage.py makemigrations

python manage.py migrate

python manage.py runserver 0:${GAME_PORT}