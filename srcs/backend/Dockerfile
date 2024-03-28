FROM python:3.12-alpine

RUN mkdir -p /var/www/django

ARG SSL_PATH=/etc/ssl/private
ARG DOMAIN=domain

#set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /var/www/django/backend

COPY tools/run_backend.sh /home/run_backend.sh
COPY tools/requirements.txt /home/requirements.txt

RUN chmod 755 /home/run_backend.sh

RUN apk update && \
    apk --no-cache add \
    openssl \
    dumb-init \
    build-base \
    libffi-dev

RUN pip install --upgrade pip
RUN pip install -r /home/requirements.txt

#RUN pip install --upgrade pip \
#    pip install django \
#    django-environ \
#    djangorestframework \
#    djangorestframework-simplejwt \
#    django-sslserver \
#    django-filter \
#    psycopg2-binary \
#    django-extensions \
#    drf-spectacular \
#    django-dotenv

#RUN openssl genrsa -out ${SSL_PATH}/${DOMAIN}.key 2048 && \
#    openssl req -new -key ${SSL_PATH}/${DOMAIN}.key -out ${SSL_PATH}/${DOMAIN}.crt \
#    -subj "/C=KR/ST=Seoul/L=Gaepodong/O=42seoul/OU=Cadet/CN=${DOMAIN}" && \
#    openssl x509 -req -days 1000 -in ${SSL_PATH}/${DOMAIN}.crt -signkey ${SSL_PATH}/${DOMAIN}.key -out ${SSL_PATH}/${DOMAIN}.crt

ENTRYPOINT ["dumb-init", "--", "/home/run_backend.sh" ]