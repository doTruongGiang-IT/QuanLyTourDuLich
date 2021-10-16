build:
	docker build -t pl_backend .

up:
	docker-compose -p travel_management up

down:
	docker-compose -p travel_management down

restart:
	docker-compose -p travel_management down
	docker-compose -p travel_management up

init:
	docker exec -it pl_backend pipenv run python3 manage.py migrate

package=
install:
	docker exec -it pl_backend pipenv install $(package)