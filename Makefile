API_SERVICE_NAME := api
DB_SERVICE_NAME := db

# docker compose

upbuild: build up

build:
	docker-compose build

up:
	docker-compose up -d

restart:
	docker-compose restart $(filter-out $@,$(MAKECMDGOALS))

down:
	docker-compose down

destroy:
	docker-compose down -v

# interactive shell

django_shell: up
	docker-compose exec ${API_SERVICE_NAME} python manage.py shell

api_shell: up
	docker-compose exec ${API_SERVICE_NAME} sh

db_shell: up
	docker-compose exec ${DB_SERVICE_NAME} sh

# logs

api_logs: up
	docker-compose logs -f ${API_SERVICE_NAME}

db_logs: up
	docker-compose logs -f ${DB_SERVICE_NAME}

# django

startapp:
	docker-compose run --rm ${API_SERVICE_NAME} python manage.py startapp $(filter-out $@,$(MAKECMDGOALS))

makemigrations:
	docker-compose run --rm ${API_SERVICE_NAME} python manage.py makemigrations $(filter-out $@,$(MAKECMDGOALS))

migrate:
	docker-compose run --rm ${API_SERVICE_NAME} python manage.py migrate $(filter-out $@,$(MAKECMDGOALS))

createsuperuser:
	docker-compose run --rm ${API_SERVICE_NAME} python manage.py createsuperuser $(filter-out $@,$(MAKECMDGOALS))

test:
	docker-compose run --rm ${API_SERVICE_NAME} python manage.py test

manage:
	docker-compose run --rm ${API_SERVICE_NAME} python manage.py $(filter-out $@,$(MAKECMDGOALS))

# lint

lint:
	flake8
