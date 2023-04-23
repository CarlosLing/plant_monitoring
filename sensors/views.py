from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse

from src.sensor_data import utils

from .models import Sensor


def index(request):
    sensor_list = list(Sensor.objects.all())
    context = {"sensor_list": sensor_list}

    return render(request, "plant_app/index.html", context)


def sensor(request, sensor_id):
    sensor = get_object_or_404(Sensor, pk=sensor_id)
    return render(request, "plant_app/sensor_detail.html", {"sensor": sensor})


def datapoint_form(request):
    sensor_list = list(Sensor.objects.all())
    context = {"sensor_list": sensor_list}
    return render(request, "plant_app/add_datapoint.html", context)


def save_datapoint(request):
    print(request.POST)
    try:
        sensor = get_object_or_404(Sensor, pk=request.POST["sensor"])
        random_reading = utils.generate_random_reading(
            sensor, max_value=100, min_value=0
        )
        print(random_reading)
    except Sensor.DoesNotExist:
        print("exception to be implemented")
        sensor_list = list(Sensor.objects.all())
        context = {"sensor_list": sensor_list, "error_message": "NO SENSOR SELECTED"}
        return render(request, "plant_app/add_datapoint.html", context)
    print(utils.random_value())
    return HttpResponseRedirect(reverse("sensors:manual_collection"))
