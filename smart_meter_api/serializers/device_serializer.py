from rest_framework import serializers
from smart_meter_api.models.device import Device

# from smart_meter_api.serializers.measurement_serializer import MeasurementSerializer


class DeviceSerializer(serializers.ModelSerializer):
    rssi = serializers.IntegerField(source="last_measurement.rssi")
    snr = serializers.FloatField(source="last_measurement.snr")
    volume = serializers.FloatField(source="last_measurement.volume")
    battery_level = serializers.FloatField(source="last_measurement.battery_level")
    created_at = serializers.DateTimeField(source="last_measurement.created_at")

    class Meta:
        model = Device
        fields = ["id", "eui", "rssi", "snr", "volume", "battery_level", "created_at"]


class DeviceMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ["id", "eui", "created_at"]
