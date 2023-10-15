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


.PHONY: run_server_docker
run_server_docker:
	echo "Starting plant server"
	docker run -p 8000:8000 -d --name plant_server_container plant_server
	echo "Plant server started on container plant_server_container"


.PHONY: start_server_docker
start_server_docker:
	echo "Resuming plant server"
	docker start plant_server_container
	echo "Plant server resumed"

.PHONY: stop_server_docker
stop_server_docker:
	echo "Stopping plant server"
	docker stop plant_server_container
	echo "Plant server started stopped"
