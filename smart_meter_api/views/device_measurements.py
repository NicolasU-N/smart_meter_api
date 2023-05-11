from rest_framework import generics
from smart_meter_api.models.measurement import Measurement
from smart_meter_api.serializers.measurement_serializer import MeasurementSerializer


class MeasurementList(generics.ListAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        device_id = self.request.query_params.get("device_id", None)
        if device_id is not None:
            queryset = queryset.filter(device_id=device_id)
        return queryset
