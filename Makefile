build:
	docker-compose -f local.yml up --build -d --remove-orphans

up:
	docker-compose -f local.yml up -d

down:
	docker-compose -f local.yml down

down-v:
	docker-compose -f local.yml down -v

makemigrations:
	docker-compose -f local.yml run --rm api python manage.py makemigrations

migrate:
	docker-compose -f local.yml run --rm api python manage.py migrate

collectstatic:
	docker-compose -f local.yml run --rm api python manage.py collectstatic --no-input --clear

superuser:
	docker-compose -f local.yml run --rm api python manage.py createsuperuser

populate-units:
	docker-compose -f local.yml run --rm api python manage.py populate_units

generate-random-users:
	docker-compose -f local.yml run --rm api python manage.py generate_random_users
