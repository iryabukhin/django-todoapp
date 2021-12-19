CURRENT_DIRECTORY := $(shell pwd)

begin: migrate start

start:
	@docker-compose up -d

stop:
	@docker-compose stop

down:
	@docker-compose down

ps:
	@docker-compose ps

restart: stop start

clean: stop
	@docker-compose rm --force
	@find . -name \*.pyc -delete

build:
	@docker-compose build web

migrate:
	@docker-compose run --rm web python3 manage.py migrate

cli:
	@docker-compose run --rm web /bin/bash

dbshell:
	@docker-compose exec db psql -Upostgres -W todoapp

logs:
	@docker-compose logs -f

.PHONY: start stop ps restart clean build migrate cli dbshell logs
