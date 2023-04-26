from django.test import TestCase
from django.urls import reverse

# Create your tests here.


class SensorListViewTest(TestCase):
    def test_no_sensors(self):
        response = self.client.get(reverse("sensors:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No sensors are available.")
        self.assertQuerySetEqual(response.context["sensor_list"], [])


# class SensorDetailViewTest(TestCase):


# class SensorDetailViewTest(TestCase):
