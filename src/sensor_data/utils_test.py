from datetime import datetime

import pytest
import pytz
from django.test import TestCase

from sensors.models import Sensor
from sensors.models import SensorReadings

from .utils import generate_random_reading
from .utils import random_value
from .utils import save_reading


class test_random_value(TestCase):
    def test_value_in_range(self):
        v_max = 10
        v_min = 0

        value = random_value(v_max, v_min)
        assert value >= v_min
        assert value <= v_max

    def test_faulty_range(self):
        v_min = 10
        v_max = 0

        with pytest.raises(ValueError):
            random_value(v_max, v_min)


class test_generate_random_reading(TestCase):
    def test_correct_date(self):
        sensor = Sensor()
        now = datetime.now()

        sensor_reading = generate_random_reading(sensor, date_time=now)
        self.assertIs(sensor_reading.timestamp, now)

    def test_correct_sensor(self):
        sensor = Sensor()
        now = datetime.now()

        sensor_reading = generate_random_reading(sensor, date_time=now)
        self.assertIs(sensor_reading.sensor, sensor)

    def test_wrong_sensor_class(self):
        sensor = 1
        now = datetime.now()

        with pytest.raises(ValueError):
            generate_random_reading(sensor, date_time=now)

    def test_no_set_time(self):
        sensor = Sensor()
        t0 = datetime.now()

        sensor_reading = generate_random_reading(sensor)
        t1 = datetime.now()

        assert t1 > sensor_reading.timestamp
        assert t0 < sensor_reading.timestamp


class test_save_reading(TestCase):
    def test_reading_saved(self):
        s1 = Sensor(name="sensor1")
        s1.save()
        value = 20.4

        utc = pytz.UTC
        t0 = datetime.now().replace(tzinfo=utc)
        save_reading(sensor=s1, value=value)
        t1 = datetime.now().replace(tzinfo=utc)

        readings = SensorReadings.objects.all()

        assert len(readings) == 1
        assert readings[0].value == value
        assert readings[0].sensor == s1
        assert t1 > readings[0].timestamp
        assert t0 < readings[0].timestamp

    def test_no_saved_sensor(self):
        s1 = Sensor(name="name")
        value = 20.4

        with pytest.raises(ValueError):
            save_reading(sensor=s1, value=value)

    def test_invalid_value(self):
        s1 = Sensor(name="sensor1")
        s1.save()
        value = "hello"

        with pytest.raises(ValueError):
            save_reading(sensor=s1, value=value)
