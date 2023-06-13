from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD

    def validate(self, attrs):
        password = attrs.get("password")
        email = attrs.get("email")

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                msg = "No active account found with the given credentials"
                raise exceptions.AuthenticationFailed(msg)

            if not user.check_password(password):
                msg = "No active account found with the given credentials"
                raise exceptions.AuthenticationFailed(msg)

            if not user.is_active:
                msg = "Account is not active"
                raise exceptions.AuthenticationFailed(msg)

        else:
            msg = 'Must include "email" and "password".'
            raise exceptions.ValidationError(msg)

        attrs["user"] = user
        return super().validate(attrs)
