from django.http import HttpResponse
from django.shortcuts import render

from .models import Sensor


def index(request):
    sensor_list = list(Sensor.objects.all())
    context = {"sensor_list": sensor_list}

    return render(request, "plant_app/index.html", context)


def sensor(request, sensor_id):
    response = f"{request}\n This is {sensor_id}"
    return HttpResponse(response)
