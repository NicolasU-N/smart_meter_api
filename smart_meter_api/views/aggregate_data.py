from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg, Sum, Count

from smart_meter_api.models.device import Device
from smart_meter_api.models.measurement import Measurement

from django.contrib.auth.models import User

from rest_framework import permissions

from django.http import Http404

# from django.db.models.functions import ExtractYear, ExtractMonth
# from django.utils import timezone
# from smart_meter_api.serializers.device_serializer import DeviceSerializer
# from smart_meter_api.serializers.measurement_serializer import MeasurementSerializer


class DeviceCountView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Device.objects.all()  # establece un valor por defecto para queryset

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404("No user found matching this id")

        user = User.objects.get(id=user_id)
        device_count = Device.objects.filter(user=user).count()
        return Response({"device_count": device_count})


class MonthlyUsageView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Measurement.objects.all()  # establece un valor por defecto para queryset

    def get(self, request, user_id, year, month):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404("No user found matching this id")

        user = User.objects.get(id=user_id)
        devices = Device.objects.filter(user=user)
        total_usage = Measurement.objects.filter(
            device__in=devices, created_at__year=year, created_at__month=month
        ).aggregate(total_volume=Sum("water_consumption"))["total_volume"]

        return Response({"total_usage": total_usage})


class MonthlyAverageUsageView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Measurement.objects.all()  # establece un valor por defecto para queryset

    def get(self, request, user_id, year, month):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404("No user found matching this id")

        user = User.objects.get(id=user_id)
        devices = Device.objects.filter(user=user)
        avg_usage = Measurement.objects.filter(
            device__in=devices, created_at__year=year, created_at__month=month
        ).aggregate(avg_volume=Avg("water_consumption"))["avg_volume"]

        return Response({"avg_usage": avg_usage})


# class UserDevicesConsumption(APIView):
#     """
#     View to get the total consumption of all devices for a user for a given month
#     """

#     def get(
#         self, request, year=timezone.now().year, month=timezone.now().month, format=None
#     ):
#         user_id = request.user.id
#         total_consumption = Measurement.objects.filter(
#             device__user_id=user_id, created_at__year=year, created_at__month=month
#         ).aggregate(Sum("volume"))
#         return Response(total_consumption)


# class UserDevicesAverageConsumption(APIView):
#     """
#     View to get the average consumption of all devices for a user for a given month
#     """

#     def get(
#         self, request, year=timezone.now().year, month=timezone.now().month, format=None
#     ):
#         user_id = request.user.id
#         average_consumption = Measurement.objects.filter(
#             device__user_id=user_id, created_at__year=year, created_at__month=month
#         ).aggregate(Avg("volume"))
#         return Response(average_consumption)


# class UserDevicesConsumptionComparison(APIView):
#     """
#     View to get the comparison of the average consumption vs actual consumption of all devices for a user for a given month
#     """

#     def get(
#         self, request, year=timezone.now().year, month=timezone.now().month, format=None
#     ):
#         user_id = request.user.id
#         consumption_data = Measurement.objects.filter(
#             device__user_id=user_id, created_at__year=year, created_at__month=month
#         ).aggregate(Avg("volume"), Sum("volume"))
#         return Response(consumption_data)


# class UserDevicesLastMonthConsumption(APIView):
#     """
#     View to get the total consumption of all devices for a user for the previous month
#     """

#     def get(
#         self,
#         request,
#         year=timezone.now().year,
#         month=timezone.now().month - 1,
#         format=None,
#     ):
#         if month == 0:
#             month = 12
#             year -= 1
#         user_id = request.user.id
#         last_month_total_consumption = Measurement.objects.filter(
#             device__user_id=user_id, created_at__year=year, created_at__month=month
#         ).aggregate(Sum("volume"))
#         return Response(last_month_total_consumption)
