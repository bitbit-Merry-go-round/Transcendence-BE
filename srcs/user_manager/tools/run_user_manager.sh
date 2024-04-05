#!/bin/sh

cat << EOF > ./.env
SECRET_KEY=${SECRET_KEY}

FOURTYTWO_CLIENT_ID=${FOURTYTWO_CLIENT_ID}
FOURTYTWO_CLIENT_SECRET=${FOURTYTWO_CLIENT_SECRET}

USERS_DB_NAME=${USERS_DB_NAME}
USERS_DB_HOST=${USERS_DB_HOST}
USERS_DB_USER=${USERS_DB_USER}
USERS_DB_PW=${USERS_DB_PW}
USERS_DB_PORT=${USERS_DB_PORT}
EOF

python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser --no-input

python ./add_user.py

python manage.py runserver 0:${USERS_DB_PORT}