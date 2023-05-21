from rest_framework import serializers

from .models import Sensor
from .models import SensorReadings


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = "__all__"


class SensorReadingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorReadings
        fields = "__all__"
