from rest_framework import serializers
from users.models import CustomUser
from django.contrib.auth.password_validation import validate_password


class OTPVerificationSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["email", "otp"]
