from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Sensor
from .models import SensorReadings
from .serializers import SensorReadingsSerializer
from .serializers import SensorSerializer


@api_view(["GET", "POST"])
def sensor_list(request):
    if request.method == "GET":
        sensors = Sensor.objects.all()
        serializer = SensorSerializer(sensors, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = SensorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST", "PUT", "DELETE"])
def sensor_readings(request, pk):
    try:
        sensor = Sensor.objects.get(pk=pk)
    except Sensor.DoesNotExist:
        return Response("Sensor does not exist", status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        readings = SensorReadings.objects.filter(sensor=sensor)
        serializer = SensorReadingsSerializer(readings, many=True)
        # Combine this into a function
        sensor_data = SensorSerializer(sensor).data
        sensor_data["datapoints"] = serializer.data
        return Response(sensor_data)
    elif request.method == "POST":
        reading_data = request.data
        reading_data["sensor"] = pk
        serializer = SensorReadingsSerializer(data=reading_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "PUT":
        reading_data = request.data
        serializer = SensorSerializer(
            sensor, data=reading_data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        sensor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
