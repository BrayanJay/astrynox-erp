.PHONY: up down build logs test migrate shell ps restart clean

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f $(service)

test:
	docker compose exec $(service) pytest tests/ -v

migrate:
	docker compose exec $(service) alembic upgrade head

shell:
	docker compose exec $(service) /bin/sh

ps:
	docker compose ps

restart:
	docker compose restart $(service)

clean:
	docker compose down -v --remove-orphans
