from datetime import datetime
from typing import Optional

import numpy as np

from sensors.models import Sensor
from sensors.models import SensorReadings


def random_value(max_value: float = 100, min_value: float = 0):
    return np.random.uniform(high=max_value, low=min_value)


def generate_random_reading(
    sensor: Sensor,
    max_value: float = 100,
    min_value: float = 0,
    date_time: Optional[datetime] = None,
) -> SensorReadings:
    value = random_value(max_value, min_value)
    sensor_reading = SensorReadings(sensor, value, date_time)
    return sensor_reading
