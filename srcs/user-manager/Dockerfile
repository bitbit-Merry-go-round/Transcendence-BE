FROM python:3.12-alpine

RUN mkdir -p /var/www/django

ARG DOMAIN=domain

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

ENTRYPOINT ["dumb-init", "--", "/home/run_user_manager.sh" ]