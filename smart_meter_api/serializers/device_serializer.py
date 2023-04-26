from rest_framework import serializers
from smart_meter_api.models.device import Device

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', '_id', 'eui', 'rssi', 'payload', 'createdAt']