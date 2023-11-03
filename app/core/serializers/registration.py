from rest_framework import serializers
from core.models import CustomUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("full_name", "email", "phone_number", "password")
        extra_kwargs = {"password": {"write_only": True}}
