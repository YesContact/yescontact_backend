from rest_framework import serializers
from core.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.full_name", read_only=True)

    class Meta:
        model = Contact
        fields = ["id", "phone_number", "user", "full_name"]
