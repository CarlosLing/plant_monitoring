from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .models import Sensor


def index(request):
    sensor_list = list(Sensor.objects.all())
    context = {"sensor_list": sensor_list}

    return render(request, "plant_app/index.html", context)


def sensor(request, sensor_id):
    sensor_id = get_object_or_404(Sensor, pk=sensor_id)
    return render(request, "plant_app/sensor_detail.html", {"sensor": sensor})
