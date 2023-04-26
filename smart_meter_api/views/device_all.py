from rest_framework import viewsets, permissions, generics

from smart_meter_api.models.device import Device
from smart_meter_api.serializers.device_serializer import DeviceSerializer

# class DevicesAll(generics.RetrieveAPIView):
#     queryset = Devices.objects.all()
#     serializer_class = DeviceSerializer


class DevicesAll(viewsets.ModelViewSet):
    queryset = Device.objects.all().order_by("id")
    serializer_class = DeviceSerializer
    permission_classes = [permissions.IsAuthenticated]
