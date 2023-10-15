FROM python:3.10-slim

RUN mkdir plant_monitoring_app
WORKDIR /plant_monitoring_app
COPY plant_app plant_app
COPY src src
COPY sensors sensors
COPY manage.py .

# Create Django Key
RUN mkdir .secrets
RUN openssl rand -hex 12 >> .secrets/django_secret_key.txt

# Install requirements
RUN pip install -r src/requirements.txt

RUN python manage.py migrate

ENTRYPOINT [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
