from rest_framework import serializers
from smart_meter_api.models.measurement import Measurement
from smart_meter_api.models.device import Device
from smart_meter_api.serializers.device_serializer import DeviceMeasurementSerializer


class MeasurementSerializer(serializers.ModelSerializer):
    device = DeviceMeasurementSerializer(read_only=True)

    class Meta:
        model = Measurement
        fields = "__all__"


# class DeviceMeasurementSerializer(serializers.ModelSerializer):
#     measurements = MeasurementSerializer(many=True, read_only=True)

#     class Meta:
#         model = Device
#         fields = "__all__"
