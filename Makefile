rebuild:
	docker compose up --force-recreate --build -d 
	docker exec -it sadoparser_bot alembic upgrade head

build:
	docker compose up -d
	docker exec -it sadoparser_bot alembic upgrade head

upgrade:
	docker exec -it sadoparser_bot alembic upgrade head
