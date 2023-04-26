from datetime import datetime

import pytest
from django.test import TestCase

from sensors.models import Sensor

from .utils import generate_random_reading
from .utils import random_value


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
