install:
	@pip install uv
	@uv sync

run:
	@uv run python3 manage.py runserver

add_app:
	@uv run python3 manage.py startapp $(APP)

makemigrations:
	@uv run python3 manage.py makemigrations

migrate:
	@uv run python3 manage.py migrate

superuser:
	@uv run python3 manage.py createsuperuser

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +

help:
	@echo "Available commands:"
	@echo "  make install                 Install project dependencies"
	@echo "  make run                     Run development server"
	@echo "  make add_app APP=app_name    Create a new Django app"
	@echo "  make makemigrations          Create migrations"
	@echo "  make migrate                 Apply migrations"
	@echo "  make superuser               Create admin user"
	@echo "  make clean                   Remove __pycache__ directories"
	@echo "  make help                    Show available commands"


.PHONY: run add_app makemigrations migrate superuser clean help