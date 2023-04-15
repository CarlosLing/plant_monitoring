from django.contrib import admin

from .models import Sensor
from .models import SensorReadings

admin.site.register(Sensor)
admin.site.register(SensorReadings)
