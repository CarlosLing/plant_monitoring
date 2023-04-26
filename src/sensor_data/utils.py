from datetime import datetime
from typing import Optional

import numpy as np

from sensors.models import Sensor
from sensors.models import SensorReadings


def random_value(max_value: float = 100, min_value: float = 0):
    if max_value < min_value:
        raise ValueError(
            f"max_value: {max_value}, should be greater or equal than min_value: {min_value}"
        )

    return np.random.uniform(high=max_value, low=min_value)


def generate_random_reading(
    sensor: Sensor,
    max_value: float = 100,
    min_value: float = 0,
    date_time: Optional[datetime] = None,
) -> SensorReadings:
    """
    Creates a random reading for the sensor provided
    input:
        - sensor:
        - max/min_value: range of values for the sensor value
        - date_time: datetime of the reading, if None current time is taken.
    """
    value = random_value(max_value, min_value)

    if date_time is None:
        date_time = datetime.now()

    sensor_reading = SensorReadings(sensor=sensor, value=value, timestamp=date_time)

    return sensor_reading
