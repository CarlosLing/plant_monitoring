from django.http import Http404
from django.shortcuts import render

from .models import Sensor


def index(request):
    sensor_list = list(Sensor.objects.all())
    context = {"sensor_list": sensor_list}

    return render(request, "plant_app/index.html", context)


def sensor(request, sensor_id):
    try:
        sensor = Sensor.objects.get(pk=sensor_id)
    except Sensor.DoesNotExist:
        raise Http404("Sensor does not exist")
    return render(request, "plant_app/sensor_detail.html", {"sensor": sensor})
