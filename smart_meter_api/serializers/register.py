from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken

from django.core.exceptions import ValidationError


def validate_username(username):
    # Puedes personalizar esta función de validación según tus necesidades.
    if len(username) < 3:
        raise ValidationError("Username must be at least 3 characters long.")
    if User.objects.filter(username=username).exists():
        raise ValidationError("Username is already taken.")


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    username = serializers.CharField(
        validators=[validate_username]
    )  # Aquí reemplazamos el validador por defecto

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    password_confirm = serializers.CharField(write_only=True, required=True)

    access = serializers.SerializerMethodField()
    refresh = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "password_confirm",
            "email",
            "first_name",
            "last_name",
            "access",
            "refresh",
        )
        extra_kwargs = {
            "first_name": {"required": False},
            "last_name": {"required": False},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            is_active=True,
        )

        user.set_password(validated_data["password"])
        user.save()

        return user

    def get_access(self, obj):
        refresh = RefreshToken.for_user(obj)
        return str(refresh.access_token)

    def get_refresh(self, obj):
        refresh = RefreshToken.for_user(obj)
        return str(refresh)
