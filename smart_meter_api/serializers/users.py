from rest_framework import serializers
from django.contrib.auth.models import User, Group
from rest_framework_simplejwt.tokens import RefreshToken


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    access = serializers.SerializerMethodField()
    refresh = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "is_staff", "access", "refresh"]

    def get_access(self, obj):
        refresh = RefreshToken.for_user(obj)
        return str(refresh.access_token)

    def get_refresh(self, obj):
        refresh = RefreshToken.for_user(obj)
        return str(refresh)


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]
