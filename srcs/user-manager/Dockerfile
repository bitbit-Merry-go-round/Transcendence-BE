FROM python:3.12-alpine

RUN mkdir -p /var/www/django

ARG DOMAIN=fresh_pong
ARG SSL_PATH=/etc/ssl/private

#set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /var/www/django/user-manager

COPY tools/run_user_manager.sh /home/run_user_manager.sh
COPY tools/requirements.txt /home/requirements.txt

RUN chmod 755 /home/run_user_manager.sh

RUN apk update && \
    apk --no-cache add \
    openssl \
    dumb-init \
    build-base \
    libffi-dev

RUN pip install --upgrade pip
RUN pip install -r /home/requirements.txt

RUN openssl genrsa -out ${SSL_PATH}/${DOMAIN}.key 2048 && \
   openssl req -new -key ${SSL_PATH}/${DOMAIN}.key -out ${SSL_PATH}/${DOMAIN}.crt \
   -subj "/C=KR/ST=Seoul/L=Gaepodong/O=42seoul/OU=Cadet/CN=${DOMAIN}" && \
   openssl x509 -req -days 1000 -in ${SSL_PATH}/${DOMAIN}.crt -signkey ${SSL_PATH}/${DOMAIN}.key -out ${SSL_PATH}/${DOMAIN}.crt

ENTRYPOINT ["dumb-init", "--", "/home/run_user_manager.sh" ]