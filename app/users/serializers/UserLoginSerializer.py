from rest_framework import serializers


class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        fields = ("phone_number", "password")
