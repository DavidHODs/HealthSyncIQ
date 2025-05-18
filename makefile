MIGRATIONS_DIR=src/database/migrations

install:
	poetry install

lint:
	poetry run autopep8 --aggressive --indent-size 2 --max-line-length 80 --in-place --recursive src/
	poetry run isort --line-length 80 --indent 2 src/
	poetry run ruff check --fix src/
	poetry run mypy src/

run:
	poetry run python src/main.py

init-db:
	poetry run alembic init $(MIGRATIONS_DIR)

makemigration:
	@if [ -z "$(NAME)" ]; then echo "Error: NAME is required. Usage: make makemigration NAME='your_migration_name'"; exit 1; fi
	poetry run alembic revision -m "$(NAME)"

migrate:
	poetry run alembic upgrade head

downgrade:
	poetry run alembic downgrade -1

db-history:
	poetry run alembic history

db-current:
	poetry run alembic current

db-stamp:
	poetry run alembic stamp head
