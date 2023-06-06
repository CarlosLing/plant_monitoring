# plant_monitoring
My plants died this winter while I was on vacation... Let's overengineer a solution so I can avoid asking a human being to take care of my plants

# Start the django server

## Install dependencies

```bash
pip install -r plant_app/src/requirements.txt
```

## Create key for django application

```bash
openssl rand -hex 12 >> .secrets/django_secret_key.txt
```

## Initial migrations

```bash
python manage.py migrate
```

## Run the server

```bash
python manage.py runserver
```

# Create sensor:
send post request as:
```json
{"name":"test-sensor", "variable":"humidity", "location": "living room", "arduino_board":"test-board", "plant":"test plant"}
```

# Create sensor readings:
send post request as:
```json
{"value":23}
```

# Contribute

## Precommit

Install pre-commit on your development machine with:
```bash
pip install pre-commit
```

Then set up the hooks with pre-commit install, when you perform your first commit the hooks will initialize and the tasks in the `pre-commit-config.yaml` will execute.

```bash
pre-commit install
```
check the if there any errors and rectify and re commit again.
