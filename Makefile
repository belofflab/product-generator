rebuild:
	docker compose up --force-recreate --build -d 
	docker exec -it generator_bot alembic upgrade head

build:
	docker compose up -d
	docker exec -it generator_bot alembic upgrade head

upgrade:
	docker exec -it generator_bot alembic upgrade head
