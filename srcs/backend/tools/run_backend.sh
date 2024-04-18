#!/bin/sh

cat << EOF > ./.env
SECRET_KEY=${SECRET_KEY}

SERVER_IP=${SERVER_IP}
FOURTYTWO_CLIENT_ID=${FOURTYTWO_CLIENT_ID}
FOURTYTWO_CLIENT_SECRET=${FOURTYTWO_CLIENT_SECRET}
FOURTYTWO_REDIRECT_URI=${FOURTYTWO_REDIRECT_URI}

BACKEND_DB_NAME=${BACKEND_DB_NAME}
BACKEND_DB_HOST=${BACKEND_DB_HOST}
BACKEND_DB_USER=${BACKEND_DB_USER}
BACKEND_DB_PW=${BACKEND_DB_PW}
BACKEND_DB_PORT=${BACKEND_DB_PORT}

USER_MANAGER_PORT=${USERS_PORT}

EMAIL_HOST=${EMAIL_HOST}
EMAIL_PORT=${EMAIL_PORT}
EMAIL_USE_TLS=${EMAIL_USE_TLS}
EMAIL_HOST_USER=${EMAIL_HOST_USER}
EMAIL_HOST_PASSWORD=${EMAIL_HOST_PASSWORD}
EOF

python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser --no-input

# todo ssl 가장 나중에 하자. 그리고 오류 생김. sslserver 구동할 수 있게 패키지 받아야 함. django settings에 INSTALLED_APP에도 설정 해야 함.
python manage.py runsslserver --certificate /etc/ssl/private/fresh_pong.crt --key /etc/ssl/private/fresh_pong.key 0:8000
# python manage.py runserver 0:8000
