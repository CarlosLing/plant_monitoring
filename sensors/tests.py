from django.test import TestCase
from django.urls import reverse

from .models import Sensor
from .models import SensorReadings

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


class APIListSensors(TestCase):
    def test_sensor_list(self):
        Sensor.objects.create(name="sensor1")

        response = self.client.get(reverse("sensors:api_sensor_list"))

        list_sensors = response.json()
        self.assertEqual(len(list_sensors), 1)

        name_sensors = [sensor["name"] for sensor in list_sensors]
        assert "sensor1" in name_sensors
        assert "sensor2" not in name_sensors

    def test_submit_sensor(self):
        response = self.client.post(
            reverse("sensors:api_sensor_list"),
            data={
                "name": "sensor1",
                "variable": "sample",
                "location": "sample",
                "arduino_board": "sample",
                "plant": "sample",
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["name"], "sensor1")

        response = self.client.get(reverse("sensors:api_sensor_list"))
        list_sensors = response.json()
        name_sensors = [sensor["name"] for sensor in list_sensors]
        assert "sensor1" in name_sensors


class APISensorReadings(TestCase):
    def test_sensor_reading_list(self):
        sensor = Sensor.objects.create(name="sensor1")
        SensorReadings.objects.create(sensor=sensor, value=1)
        Sensor.objects.create(name="sensor1")
        response = self.client.get(
            reverse("sensors:api_sensor_readings_list", args=(sensor.id,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["datapoints"]), 1)

    def test_sensor_rename(self):
        sensor = Sensor.objects.create(name="sensor1")
        response = self.client.put(
            reverse("sensors:api_sensor_readings_list", args=(sensor.id,)),
            data={
                "name": "sensor-renamed",
                "variable": "sample",
                "location": "sample",
                "arduino_board": "sample",
                "plant": "sample",
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 204)
        new_sensor = Sensor.objects.all()[0]
        self.assertEqual(new_sensor.name, "sensor-renamed")

    def test_sensor_delete(self):
        sensor = Sensor.objects.create(name="sensor1")
        self.assertEqual(len(Sensor.objects.all()), 1)
        response = self.client.delete(
            reverse("sensors:api_sensor_readings_list", args=(sensor.id,))
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(Sensor.objects.all()), 0)

    def test_sensor_reading_create(self):
        sensor = Sensor.objects.create(name="sensor1")
        response = self.client.post(
            reverse("sensors:api_sensor_readings_list", args=(sensor.id,)),
            data={
                "value": 1,
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["value"], 1)

        response = self.client.get(
            reverse("sensors:api_sensor_readings_list", args=(sensor.id,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["datapoints"]), 1)

    def test_sensor_not_exist(self):
        response = self.client.get(
            reverse("sensors:api_sensor_readings_list", args=("1",))
        )
        self.assertEqual(response.status_code, 404)


# TODO: test for displaying value interface
# Test that when calling the interface the list of available sensors is passed as a context
# Test that when an error is passed the message is somewhere in the HTML code
# class SensorManualInputTest(TestCase):

# TODO: test for creating random sensor values
# Test that the post request creates a Sensor Reading value
# Test that a sensor that is not in the database will NOT be saved
# class SensorSaveValuesTest(TestCase):
