# Locally
.PHONY: install
install:
	poetry install
	poetry run pre-commit install

.PHONY: run_server
run_server:
	poetry run python manage.py runserver

# Build and run server
.PHONY: build_server_docker
build_server_docker:
	docker build -t plant_server .
