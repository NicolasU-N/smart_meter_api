from rest_framework import generics
from smart_meter_api.models.measurement import Measurement
from smart_meter_api.serializers.measurement_serializer import MeasurementSerializer

from django.db.models import Q
from datetime import datetime, timedelta


class MeasurementList(generics.ListAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        device_id = self.request.query_params.get("device_id", None)
        if device_id is not None:
            queryset = queryset.filter(device_id=device_id)
        return queryset

class CurrentWeekMeasurementsList(generics.ListAPIView):
    serializer_class = MeasurementSerializer

    def get_queryset(self):
        now = datetime.now()
        start_week = now - timedelta(days=now.weekday())
        end_week = start_week + timedelta(days=6)
        # debug start_week and end_week
        # print("start_week: ", start_week)
        # print("end_week: ", end_week)
        queryset = Measurement.objects.filter(Q(created_at__range=(start_week, end_week)) & Q(device_id=self.kwargs['device_id']))
        return queryset


class LastWeekMeasurementsList(generics.ListAPIView):
    serializer_class = MeasurementSerializer

    def get_queryset(self):
        now = datetime.now()
        start_last_week = now - timedelta(days=now.weekday() + 7)
        end_last_week = start_last_week + timedelta(days=6)
        # print("start_last_week: ", start_last_week) # debug
        # print("end_last_week: ", end_last_week)
        queryset = Measurement.objects.filter(Q(created_at__range=(start_last_week, end_last_week)) & Q(device_id=self.kwargs['device_id']))
        return queryset