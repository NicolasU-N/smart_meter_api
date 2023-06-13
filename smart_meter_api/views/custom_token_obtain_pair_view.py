from rest_framework_simplejwt.views import TokenObtainPairView
from smart_meter_api.serializers.custom_token_obtain_pair_serializer import (
    CustomTokenObtainPairSerializer,
)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
