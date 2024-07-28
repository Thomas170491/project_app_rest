from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import *

# accounts/serializers.py


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "name",
            "email",
            "phone_number",
            "role",
            "is_superuser",
        ]


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(style={"input_type": "password"})

    def validate(self, data):
        username = data.get("username").lower()
        password = data.get("password")
        try:
            user = User.objects.get(username=username)
            user = authenticate(
                request=self.context.get("request"),
                username=user.username,
                password=password,
            )
            if user:
                data["user"] = user
            else:
                raise serializers.ValidationError("Invalid credentials")
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials of user")
        return data


class VehicleSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Vehicle
        fields = ["id", "user", "make", "year", "category", "is_booked"]


class NotificationSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = [
            "id",
            "sender",
            "receiver",
            "message_sender",
            "message_receiver",
            "order",
            "is_read",
        ]


class PaySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    driver = UserSerializer(read_only=True)

    class Meta:
        model = Payments
        fields = [
            "id",
            "user",
            "driver",
            "order",
            "total_price",
            "extra",
            "is_paid",
        ]
