from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=50)
    variable = models.CharField(max_length=50)  # "Temperature", "Humidity" ...
    location = models.CharField(max_length=50)
    arduino_board = models.CharField(max_length=50)
    plant = models.CharField(max_length=50)


class SensorValues(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.SET_NULL)
    value = models.FloatField()
    timestamp = models.TimeField()
