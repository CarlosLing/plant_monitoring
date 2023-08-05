from django.urls import path

from . import api
from . import views

app_name = "sensors"
urlpatterns = [
    path("", views.index, name="index"),
    path("detail/<int:sensor_id>/", views.sensor, name="sensor"),
    path(
        "manual_datapoint_collection/", views.datapoint_form, name="manual_collection"
    ),
    path("save_datapoint/", views.save_datapoint, name="save_datapoint"),
    path("save_sensor_data/", views.save_sensor_data, name="save_sensor_data"),
    path("api/sensors", api.sensor_list, name="api_sensor_list"),
    path(
        "api/sensors/<int:pk>",
        api.sensor_readings,
        name="api_sensor_readings_list",
    ),
]
