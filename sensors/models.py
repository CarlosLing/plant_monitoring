from django.db import models


class Sensor(models.Model):
    """
    Class to keep sensor informations:
        - name: sensor name
        - variable: variable to measure
        - location: location in the house where the sensor is located
        - arduino board: name of board to which the sensor is connected
        - plant: name of the plant that the sensor measures
    """

    name = models.CharField(max_length=50)
    variable = models.CharField(max_length=50)  # "Temperature", "Humidity" ...
    location = models.CharField(max_length=50)
    arduino_board = models.CharField(max_length=50)
    plant = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class SensorReadings(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    value = models.FloatField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.sensor}_{self.value}"
