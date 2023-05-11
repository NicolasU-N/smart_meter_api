from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from smart_meter_api.views.users import UserViewSet
from smart_meter_api.views.register import RegisterUserAPIView
from smart_meter_api.views.logout import LogoutView
from smart_meter_api.views.device_all import DeviceViewSet
from smart_meter_api.views.device_measurements import MeasurementList


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r"users", UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegisterUserAPIView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("devices/", DeviceViewSet.as_view({"get": "list"}), name="devices"),
    # {"get": "list"}
    path("measurements/", MeasurementList.as_view(), name="measurement-list"),
]
