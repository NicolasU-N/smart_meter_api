from rest_framework import viewsets, permissions, generics
from django.db.models import Subquery, OuterRef
from smart_meter_api.models.device import Device
from smart_meter_api.models.measurement import Measurement
from smart_meter_api.serializers.device_serializer import DeviceSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.annotate(
        last_measurement_rssi=Subquery(
            Measurement.objects.filter(device=OuterRef("pk"))
            .order_by("-created_at")
            .values("rssi")[:1]
        ),
        last_measurement_snr=Subquery(
            Measurement.objects.filter(device=OuterRef("pk"))
            .order_by("-created_at")
            .values("snr")[:1]
        ),
        last_measurement_volume=Subquery(
            Measurement.objects.filter(device=OuterRef("pk"))
            .order_by("-created_at")
            .values("volume")[:1]
        ),
        last_measurement_batt_level=Subquery(
            Measurement.objects.filter(device=OuterRef("pk"))
            .order_by("-created_at")
            .values("battery_level")[:1]
        ),
        last_measurement_created_at=Subquery(
            Measurement.objects.filter(device=OuterRef("pk"))
            .order_by("-created_at")
            .values("created_at")[:1]
        ),
    ).order_by("id")
    serializer_class = DeviceSerializer
    permission_classes = [permissions.IsAuthenticated]
    # pagination_class = Paginator
