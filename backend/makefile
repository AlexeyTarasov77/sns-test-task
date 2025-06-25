
run:
	poetry run python src/main.py

test:
	cp .env.test .env && poetry run pytest src/

migrations/run:
	poetry run alembic upgrade head

docker/up:
	docker compose -f docker-compose.dev.yaml up 

docker/build:
	docker compose -f docker-compose.dev.yaml up --build

docker/stop:
	docker compose -f docker-compose.dev.yaml down

docker/run-migrations:
	docker compose -f docker-compose.dev.yaml exec app alembic upgrade head

docker/test:
	docker compose -f docker-compose.dev.yaml exec app pytest

