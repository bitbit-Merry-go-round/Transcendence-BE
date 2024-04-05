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

# todo ssl 가장 나중에 하자. 그리고 오류 생김. sslserver 구동할 수 있게 패키지 받아야 함. django settings에 INSTALLED_APP에도 설정 해야 함.
# python manage.py runsslserver --certificate /etc/ssl/private/domain.crt --key /etc/ssl/private/domain.key 0:8000
python manage.py runserver 0:8000
