from django.test import TestCase
from django.urls import reverse

from .models import Sensor

# Create your tests here.


class SensorListViewTest(TestCase):
    def test_no_sensors(self):
        response = self.client.get(reverse("sensors:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No sensors are available.")
        self.assertQuerySetEqual(response.context["sensor_list"], [])

    def test_list_sensors(self):
        Sensor.objects.create(name="sensor1")
        Sensor.objects.create(name="sensor2")

        response = self.client.get(reverse("sensors:index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["sensor_list"]), 2)


class SensorDetailViewTest(TestCase):
    def test_sensor_exist(self):
        sensor = Sensor.objects.create(name="sensor1")

        response = self.client.get(reverse("sensors:sensor", args=(sensor.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "sensor1")

    def test_sensor_not_exist(self):
        response = self.client.get(reverse("sensors:sensor", args=(1,)))
        self.assertEqual(response.status_code, 404)


# TODO: test for displaying value interface
# Test that when calling the interface the list of available sensors is passed as a context
# Test that when an error is passed the message is somewhere in the HTML code
# class SensorManualInputTest(TestCase):

# TODO: test for creating random sensor values
# Test that the post request creates a Sensor Reading value
# Test that a sensor that is not in the database will NOT be saved
# class SensorSaveValuesTest(TestCase):
