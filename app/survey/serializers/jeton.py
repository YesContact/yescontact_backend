from rest_framework import serializers


class JetonConverterSerializer(serializers.Serializer):
    dollar = serializers.IntegerField()
