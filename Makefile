DOCKER_ID := $(shell docker ps -aq)
DOCKER_IMAGE_ID := $(shell docker images -q)
DOCKER_VOLUME := $(shell docker volume ls -q)
PWD := $(shell pwd)
USERS_VOL_PATH := $(PWD)/srcs/backend/srcs

all:
# todo 당신이 어느 환경에 있든 볼륨에 연결해 드립니다.
	sed -i '' 's|^\(USERS_DB_VOL_PATH\).*|USERS_DB_VOL_PATH=$(USERS_DB_VOL_PATH)|' './srcs/.env'
	sed -i '' 's|^\(USERS_VOL_PATH\).*|USERS_VOL_PATH=$(USERS_VOL_PATH)|' './srcs/.env'
	docker compose -f srcs/compose.yaml up -d

up:
	docker compose -f srcs/compose.yaml up -d

down:
	docker compose -f srcs/compose.yaml down

re: fclean
	make all

fclean:
	$(if $(DOCKER_ID), docker rm -f $(DOCKER_ID))
	$(if $(DOCKER_VOLUME), docker volume rm $(DOCKER_VOLUME))
# todo 지울 이미지 수기 작성 하셈
	docker rmi django
# docker system prune -af
# $(if $(DOCKER_IMAGE_ID), docker rmi $(DOCKER_IMAGE_ID))

django:
	docker compose -f srcs/compose.yaml run -it django sh

.PHONY: all up down re fclean